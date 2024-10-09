import glob
import os
from typing import Optional
from argparse import ArgumentParser
from tempfile import TemporaryDirectory


def get_parser():
    parser = ArgumentParser(
        prog="sphinx-runpython command line",
        description="A collection of quick tools.",
        epilog="",
    )
    parser.add_argument(
        "command",
        help="Command to run, only 'nb2py', 'readme', 'img2pdf', 'latex' are available",
    )
    parser.add_argument(
        "-p", "--path", help="Folder or file which contains the files to process"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        help="Recursive search.",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output",
    )
    parser.add_argument(
        "--zoom",
        default=1.0,
        help="reduce images when img2pdf is used",
    )
    parser.add_argument(
        "--rotate",
        default=0.0,
        help="rotate the image",
    )
    parser.add_argument("-v", "--verbose", help="verbosity", default=1, type=int)
    return parser


def nb2py(infolder: str, recursive: bool = False, verbose: int = 0):
    from .convert import convert_ipynb_to_gallery

    if not os.path.exists(infolder):
        raise FileNotFoundError(f"Unable to find {infolder!r}.")
    patterns = [infolder + "/*.ipynb", infolder + "/**/*.ipynb"]
    for pattern in patterns:
        if verbose:
            print(f"[nb2py] look with pattern {pattern!r}, recursive={recursive}")
        for name in glob.iglob(pattern, recursive=recursive):
            spl = os.path.splitext(name)
            out = spl[0] + ".py"
            if verbose:
                print(f"process {name!r} -> {out!r}")
                convert_ipynb_to_gallery(name, outfile=out)


def latex_process(
    infolder: str,
    recursive: bool = False,
    output: Optional[str] = None,
    verbose: int = 0,
):
    from .tools.latex_functions import replace_latex_command

    if not os.path.exists(infolder):
        raise FileNotFoundError(f"Unable to find {infolder!r}.")
    patterns = [infolder + "/*.rst", infolder + "/**/*.py"]
    for pattern in patterns:
        if verbose:
            print(f"[latex] look with pattern {pattern!r}, recursive={recursive}")
        for name in glob.iglob(pattern, recursive=recursive):
            with open(name, "r") as f:
                content = f.read()
            new_content = replace_latex_command(content)
            if new_content != content:
                if output:
                    new_name = os.path.join(output, os.path.split(name)[-1])
                    if verbose:
                        print(f"[latex] write {new_name!r}")
                    with open(new_name, "w") as f:
                        f.write(new_content)
                else:
                    if verbose:
                        print(f"[latex] replace inplace {name!r}")
                    with open(name, "w") as f:
                        f.write(new_content)


def process_args(args):
    cmd = args.command
    if cmd == "nb2py":
        nb2py(args.path, recursive=args.recursive, verbose=args.verbose)
        return
    if cmd == "latex":
        latex_process(
            args.path,
            recursive=args.recursive,
            verbose=args.verbose,
            ouptut=args.output,
        )
        return
    if cmd == "img2pdf":
        from .tools.img_export import images2pdf

        images2pdf(
            args.path,
            args.output,
            verbose=args.verbose,
            zoom=float(args.zoom),
            rotate=float(args.rotate),
        )
        return
    if cmd == "readme":
        from .readme import check_readme_syntax

        with TemporaryDirectory() as temp:
            check_readme_syntax(args.path, verbose=args.verbose, folder=temp)
        return
    raise ValueError(f"Command {cmd!r} is unknown.")


def main():
    parser = get_parser()
    args = parser.parse_args()
    process_args(args)
