import glob
import os
from argparse import ArgumentParser
from .convert import convert_ipynb_to_gallery


def get_parser():
    parser = ArgumentParser(
        prog="sphinx-runpython command line",
        description="A collection of quick tools.",
        epilog="",
    )
    parser.add_argument("command", help="Command to run, only nb2rst is available")
    parser.add_argument(
        "-p", "--path", help="Folder which contains the files to process"
    )
    parser.add_argument(
        "-r", "--recursive", help="Recursive search.", action="store_true"
    )
    parser.add_argument("-v", "--verbose", help="verbosity", default=1, type=int)
    return parser


def nb2rst(infolder: str, recursive: bool = False, verbose: int = 0):
    if not os.path.exists(infolder):
        raise FileNotFoundError(f"Unable to find {infolder!r}.")
    pattern = infolder + "/**/*.ipynb"
    if verbose:
        print(f"nb2rst: look with pattern {pattern!r}, recursive={recursive}")
    for name in glob.iglob(pattern, recursive=recursive):
        spl = os.path.splitext(name)
        out = spl[0] + ".rst"
        if verbose:
            print(f"process {name!r} -> {out!r}")
            convert_ipynb_to_gallery(name, outfile=out)


def process_args(args):
    cmd = args.command
    if cmd == "nb2rst":
        nb2rst(args.path, recursive=args.recursive, verbose=args.verbose)
        return
    raise ValueError(f"Command {cmd!r} is unknown.")


def main():
    parser = get_parser()
    args = parser.parse_args()
    process_args(args)
