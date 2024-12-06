import argparse
import os

from quicks import __version__, get_env, parse_template, process_project


def run():
    arg_parser = argparse.ArgumentParser(
        "Quicks", description="Project generator {}".format(__version__)
    )
    arg_parser.add_argument("template", type=str)
    arg_parser.add_argument("project", type=str)
    arg_parser.add_argument("--path", "-p", type=str)
    args = arg_parser.parse_args()
    process_project(
        get_env(),
        args.path or os.getcwd(),
        args.project,
        parse_template(args.template),
        True,
    )
