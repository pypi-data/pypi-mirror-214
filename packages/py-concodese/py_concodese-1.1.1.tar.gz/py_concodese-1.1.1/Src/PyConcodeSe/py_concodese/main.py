"""this script is just a demonstration of how to get data from the pyconcodese module"""

from __future__ import annotations
import logging
import os.path
import pathlib
import shutil
import sys
from string import Template

from py_concodese.ez_multiprocessing.ez_multi_processor import EzMultiProcessor
from py_concodese.storage.filebase import FileBase
from py_concodese.lucene_handler.lucene_helper import LuceneHelper
from py_concodese.lucene_handler.spacy_helper import SpacyHelper
from py_concodese.storage.sql_connector import SqlConnector
from py_concodese.scoring.vsm import VSM
from py_concodese.scoring.make_scoring_configs import make_scoring_configs
from py_concodese.combined_funcs.indexer import Indexer
from py_concodese.jvm_loader.jvm_loader import JVMLoader
from py_concodese.git_utils.grammar_downloader import GitGrammarDownloader

# Regular code imports
from py_concodese.tokenizers.parser_factory import ParserFactory as ParserFactory
from py_concodese.bug_parsing.bug_report import parse_bug_repository

import toml
from datetime import datetime
import cProfile
from sys import argv
from os.path import join, isdir, isfile
from pathlib import Path
from py_concodese.scoring.evaluation import (
    calc_bug_result,
    calc_map_mrr_from_incorrect_csv,
    calc_results_for_all_bug_reports,
    write_mulitple_scoring_results_to_csv,
    write_incorrect_map_mrr_comparer_csv,
)

# if this file is ever moved, this is going to break
SCRIPT_DIR = Path(__file__).parent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def main(
    reindex, file_based_sql, first_br, evaluate_all, altscoring, showscores, CFG
) -> None:
    """
    Starts the cli app

    Args:
        reindex - bool, whether to retokenize source paths
        file_based_sql - bool, whether to store the data in a persistent db
        first_br - automatically evaluate the first bug report from the repo
        evaluate_all - automatically eval whole bug repo
        altscoring - run the alternative scoring evaluation
        showscores - show more details individual category scores
        CFG - dictionary of configuration settings (see config_example.toml)
    """

    logger.info(f"application started at: {datetime.now()}")

    # take paths that are relative and make them absolute so that it doesn't
    # matter where people might try to run main.py from
    GRAMMAR_PATH = join(SCRIPT_DIR, CFG["py-concodese"]["grammar_path"])
    SQLITE_PATH = join(SCRIPT_DIR, CFG["py-concodese"]["sqlite_path"])
    DERBY_PATH = join(SCRIPT_DIR, CFG["py-concodese"]["derby_path"])
    VSM_PATH = join(SCRIPT_DIR, CFG["py-concodese"]["vsm_path"])
    OUTPUT_PATH = join(SCRIPT_DIR, CFG["py-concodese"]["output_path"])

    # # import required java modules into JVM
    # class_path = join(SCRIPT_DIR, "jars/*")
    # addClassPath(class_path)

    java_loader = JVMLoader()
    java_loader.load_basic_jars()

    # create a multicore processing handler
    ez_mp = EzMultiProcessor(CFG["misc"]["processes"], java_loader.get_classpath())



    try:
        java_loader.start_jvm()

        # initialise either Spacy helper or Lucene helper and sql connection classes
        if CFG["bug_reports"]["use_spacy"]:
            logger.info("Using Spacy tokenizer")
            tokenizer_helper = SpacyHelper(CFG["bug_reports"]["minimum_term_length"])
        else:
            logger.info("Using Lucene tokenizer")
            tokenizer_helper = LuceneHelper(CFG["bug_reports"]["minimum_term_length"])
        sql_connector = SqlConnector(
            file_based=file_based_sql,
            sqlite_dir=SQLITE_PATH,
            clean_db=reindex,  # clean the db when reindex is true
        )
        # Get grammars from Git repositories
        get_or_update_gammars(GRAMMAR_PATH)

        src_files = None

        parser_factory = ParserFactory(GRAMMAR_PATH)
        indexer = Indexer(parser_factory, sql_connector)

        if reindex:
            # read source code and store tokens in the database
            if CFG["tokenization"]["use_jim"]:
                src_files = indexer.reindex_src_with_jim(
                    src_path=CFG["dataset"]["src_path"],
                    VSM_path=VSM_PATH,
                    derby_path=DERBY_PATH,
                    delete_derby_db_after=False
                    )

                # src_files = reindex_src_with_jim(
                #     src_path=CFG["dataset"]["src_path"],
                #     grammar_path=GRAMMAR_PATH,
                #     VSM_path=VSM_PATH,
                #     sql_connector=sql_connector,
                #     derby_path=DERBY_PATH,
                #     delete_derby_db_after=False,
                # )
            else:
                src_files = indexer.reindex_src(
                    src_path=CFG["dataset"]["src_path"],
                    src_languages=CFG["dataset"]["src_languages"],
                    VSM_path=VSM_PATH
                )
                # src_files = reindex_src(
                #     src_path=CFG["dataset"]["src_path"],
                #     src_languages=CFG["dataset"]["src_languages"],
                #     grammar_path=GRAMMAR_PATH,
                #     VSM_path=VSM_PATH,
                #     sql_connector=sql_connector,
                # )

        # read bug reports
        bug_reports = parse_bug_repository(
            file_path=CFG["dataset"]["bug_repository_file"],
            lucene_helper=tokenizer_helper,
            inc_dup_terms=CFG["bug_reports"]["score_duplicate_terms"],
        )

        # It is key to the token caching that the src_files are only gathered once then reused,
        if src_files is None:
            src_files = sql_connector.get_src_files()

        # precache tokens
        if CFG["misc"]["processes"] > 1:
            logger.info("Caching src file terms")
            src_files = [FileBase.pre_cache_terms(src_file) for src_file in src_files]

        vsm = VSM(VSM_PATH)
        # calculate VSM ranks before use
        if CFG["vsm"]["precache_ranks"]:
            logger.info("Caching vsm data for all bug reports")
            vsm.precache_vsm_ranks(bug_reports)

        # initialise the lexical similarity scoring configuration
        alt_lex_sim = CFG.get("scoring", {}).get("alt_lex_sim", False)
        default_scoring_cfg = None
        if alt_lex_sim:
            default_scoring_cfg = make_scoring_configs(
                toml.load(f"config_scoring.toml")
            )[0]

        logger.info(f"initialisation complete: {datetime.now()}")

        # for a test bug report, calculate file scores
        if first_br:
            br = bug_reports[0]
            print(f"Showing test output for bug report: ")
            result = calc_bug_result(
                br, src_files, vsm, alt_lex_sim, default_scoring_cfg
            )
            result.pretty_print()
        if evaluate_all:
            calc_results_for_all_bug_reports(
                bug_reports,
                src_files,
                scoring_cfg=default_scoring_cfg,
                alt_lex_sim=alt_lex_sim,
                print_summary=True,
                vsm_path=VSM_PATH,
                summary_to_csv=CFG["py-concodese"]["save_summary"],
                full_to_csv=CFG["py-concodese"]["save_full_results"],
                csv_output_path=OUTPUT_PATH,
            )
            return
        if altscoring:
            # make scoring cfgs
            scoring_cfgs = make_scoring_configs(toml.load(f"config_scoring.toml"))
            print(f"configs to process: {len(scoring_cfgs)}")
            ez_mp.set_args(
                [
                    (bug_reports, src_files, scoring_cfg, alt_lex_sim, vsm)
                    for scoring_cfg in scoring_cfgs
                ]
            )
            summaries = ez_mp.execute_function(
                calc_results_for_all_bug_reports, start_jvm=False
            )
            write_mulitple_scoring_results_to_csv(
                csv_output_path=OUTPUT_PATH,
                summaries=summaries,
            )
            return

        valid_br_ids = [br.bug_id for br in bug_reports]

        # prompt user and generate file scores for request bug reports
        while True:
            br_id = get_id_input()
            if br_id == "exit":
                break
            if br_id == "all":
                calc_results_for_all_bug_reports(
                    bug_reports,
                    src_files,
                    default_scoring_cfg,
                    alt_lex_sim,
                    vsm_path=VSM_PATH,
                    print_summary=True,
                    summary_to_csv=CFG["py-concodese"]["save_summary"],
                    full_to_csv=CFG["py-concodese"]["save_full_results"],
                    csv_output_path=OUTPUT_PATH,
                )
                continue
            if br_id == "makemapcsv":
                write_incorrect_map_mrr_comparer_csv(
                    bug_reports,
                    src_files,
                    vsm_path=VSM_PATH,
                    csv_output_path=OUTPUT_PATH,
                )
                continue
            if br_id == "usemapcsv":
                calc_map_mrr_from_incorrect_csv(
                    csv_output_path=OUTPUT_PATH,
                )
                continue
            matching_brs = [br for br in bug_reports if br.bug_id == br_id]
            if len(matching_brs) > 0:
                result = calc_bug_result(
                    matching_brs[0],
                    src_files,
                    vsm,
                    alt_lex_sim,
                    default_scoring_cfg,
                    showscores,
                )
                result.pretty_print()
            else:
                print(
                    f"a bug report with that id could not be found in the bug "
                    f"repository valid ids are:\n{valid_br_ids}"
                )

    except Exception as ex:
        logger.exception(ex)
    finally:
        java_loader.stop_jvm()
        print(f"ended at: {datetime.now()}")


def get_user_input_settings() -> tuple[bool, bool]:
    """queries the user about reindex and data storage preferences

    returns a bool tuple: reindex, file_based_sql
    """
    reindex = True
    file_based_sql = True

    inp_reindex = input(
        f"Do you want to re index the source? (This is not necessary if you "
        f"are testing the source code you most recently indexed)"
        f"? [Y/n] "
    )

    if inp_reindex.lower() == "n":
        reindex = False
        print("The existing database will be used")
    else:
        inp_file_based = input(
            "Do you want to store the tokenization results in a persistent database? [Y/n] "
        )
        if inp_file_based.lower() == "n":
            file_based_sql = False

    return reindex, file_based_sql


def get_id_input() -> str:
    """prompts user for a valid bug id and returns the user's input"""
    print()
    inp = input("Enter a bug id, type 'all', or 'exit': ")
    inp = inp.strip()
    return inp


def check_dataset_vars(config_dict, reindex) -> dict:
    """checks the config dictionary and prompts user for any missing dataset variables

    returns a dictionary with 3 keys:
        - src_path -> str
        - bug_repository_file -> str
        - src_languages -> [str]
    """
    dataset_vars = config_dict.get("dataset", {})

    if reindex:
        add_src_path_to_dataset_vars(dataset_vars)
        grammar_path = config_dict["py-concodese"]["grammar_path"]
        add_src_languages_to_dataset_vars(dataset_vars, get_available_languages_names(grammar_path))

    add_bug_repository_file_to_dataset_vars(dataset_vars)

    config_dict["dataset"] = dataset_vars

def get_available_languages_names(grammar_path):
    parser_factory = ParserFactory(grammar_path)
    return parser_factory.get_available_languages_names()


def add_src_path_to_dataset_vars(dataset_vars) -> None:
    """gives the user the opportunity to add a src path, if one isn't present in the config

    Args:
        dataset_vars (dict):
    """
    while not isdir(dataset_vars.get("src_path", "")):
        inp = input("Enter the location of the source code you wish to analyze: ")
        inp = inp.strip()
        if isdir(inp):
            dataset_vars["src_path"] = inp
            break
        else:
            print("No directory found at that location.")


def add_bug_repository_file_to_dataset_vars(dataset_vars):
    """gives the user the opportunity to add a bug repo path
    , if one isn't present in the config

    Args:
        dataset_vars (dict):
    """
    while not isfile(dataset_vars.get("bug_repository_file", "")):
        inp = input("Enter the file location of the bug repository: ")
        inp = inp.strip()
        if isfile(inp):
            dataset_vars["bug_repository_file"] = inp
        else:
            print("No file found at that location.")


def add_src_languages_to_dataset_vars(dataset_vars, available_languages_names):
    """prompts user to select which languages are used in the src

    Args:
        dataset_vars (dict):
    """
    # make sure there's an initialised list in in the dictionary
    dataset_vars["src_languages"] = dataset_vars.get("src_languages", [])

    while len(dataset_vars["src_languages"]) == 0:
        for name in available_languages_names:
        # for name in language_string_to_enum.keys():
            inp = input(f"Does your project include source code in {name}? [y/N]: ")
            if inp.lower() == "y":
                # make a list of strings, that's what the config would contain
                # if languages were listed there
                dataset_vars["src_languages"].append(name)


def get_or_update_gammars(grammars_folder):
    """prompts user to confirm downloading the tree-sitter grammars or update the existing ones

    """

    inp = input(f"Do you want to update the grammars folder with the respective git repositories? [y/N]: ")
    if inp.lower() == "y":

        git_downloader = GitGrammarDownloader(grammars_folder)
        repositories = git_downloader.get_repositories()
        git_downloader.pull_grammars(repositories)


def get_run_parameters():
    #global profile, first, all, altscoring, showscores, CFG, reindex, file_based_sql
    print(
        "\nPossible running arguments:\n\n"
        "profile: creates a profile file after running\n"
        "first: automatically retrieves src files for first bug report\n"
        "all: automatically evaluates and scores all bug reports\n"
        "altscoring: automatically evaluates different scoring methods\n"
        "showscores: when an individual bug report is evaluated, detailed "
        "scoring information is printed to the console\n"
    )
    profile = "profile" in argv
    first = "first" in argv
    all = "all" in argv
    altscoring = "altscoring" in argv
    showscores = "showscores" in argv
    if profile:
        print("Running in profile mode. Use snakeviz to check the results.")
    CFG = toml.load(f"config.toml")
    reindex, file_based_sql = get_user_input_settings()
    check_dataset_vars(config_dict=CFG, reindex=reindex)
    main_func = lambda: main(
        reindex,
        file_based_sql,
        first_br=first,
        evaluate_all=all,
        altscoring=altscoring,
        showscores=showscores,
        CFG=CFG,
    )
    if profile:
        with cProfile.Profile() as pr:
            main_func()
            pr.dump_stats("profile_results.prof")
    else:
        main_func()


def check_config_toml_file():
    current_path = pathlib.Path('.').parent.resolve()
    config_toml_path = os.path.join(current_path, 'config.toml')
    if not os.path.exists(config_toml_path):
        create_example = input("The PyConcodese config file 'config.toml' was not found in this path. \n Do you want to copy an example file here? [y/N]")
        if create_example.lower() == "y":
            _create_config_example_with_prefilled_custom_values(config_toml_path, current_path)
            print('Example config.toml file copied in the current directory.  \n Please make sure you change the fields accordingly')
        sys.exit()


def _create_config_example_with_prefilled_custom_values(config_toml_path, current_path):
    main_path = pathlib.Path(__file__).parent.resolve()
    example_toml = os.path.join(main_path, 'examples', 'config.toml')
    d = {
        'grammars_path': os.path.join(current_path, 'Grammars'),
        'project_path': str(current_path),
        'derby_path': os.path.join(current_path, 'derby'),
        'bug_repository_file': os.path.join(current_path, 'bug_repository_file.xml'),
    }
    with open(example_toml, 'r') as f:
        src = Template(f.read())
        custom_toml = src.substitute(d)
    with open(config_toml_path, 'w') as f:
        f.writelines(custom_toml)


def main_pip_runner():
    check_config_toml_file()
    get_run_parameters()


if __name__ == "__main__":
    main_pip_runner()
