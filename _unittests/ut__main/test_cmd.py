import platform
import shutil
import sys
import tempfile
import unittest
import os
from argparse import Namespace
from sphinx_runpython.ext_test_case import ExtTestCase, hide_stdout, skipif_ci_windows
from sphinx_runpython._cmd_helper import (
    get_parser,
    nb2py,
    latex_process,
    process_args,
    sphinx_api,
)


class TestCmd(ExtTestCase):
    def test_cmd(self):
        parser = get_parser()
        self.assertNotEmpty(parser)

    @unittest.skipIf(platform.system() != "Linux", reason="pandoc not installed")
    @hide_stdout()
    def test_convert(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        nb2py(data, verbose=1)
        expected = os.path.join(data, "float_and_double_rouding.py")
        self.assertExists(expected)

    @hide_stdout()
    def test_latex(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        folder = "test_latex"
        if not os.path.exists(folder):
            os.mkdir(folder)
        latex_process(data, verbose=1, output=folder)
        expected = os.path.join(folder, "strategie_avec_alea.rst")
        self.assertExists(expected)
        expected = os.path.join(folder, "poulet.py")
        self.assertExists(expected)

    def test_latex_inplace(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copy(
                os.path.join(data, "strategie_avec_alea.rst"),
                os.path.join(tmpdir, "strategie_avec_alea.rst"),
            )
            latex_process(tmpdir, verbose=1)
            self.assertExists(os.path.join(tmpdir, "strategie_avec_alea.rst"))

    def test_nb2py_not_found(self):
        self.assertRaise(lambda: nb2py("/nonexistent/path/xyz"), FileNotFoundError)

    def test_latex_process_not_found(self):
        self.assertRaise(
            lambda: latex_process("/nonexistent/path/xyz"), FileNotFoundError
        )

    def test_process_args_nb2py_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = Namespace(
                command="nb2py",
                path=tmpdir,
                recursive=False,
                verbose=0,
            )
            process_args(args)

    @skipif_ci_windows("readme processing does not work on Windows")
    def test_process_args_readme(self):
        readme = os.path.join(os.path.dirname(__file__), "..", "..", "README.rst")
        args = Namespace(
            command="readme",
            path=readme,
            verbose=0,
        )
        process_args(args)

    def test_process_args_unknown_command(self):
        args = Namespace(command="unknown_cmd", path=None, verbose=0)
        self.assertRaise(lambda: process_args(args), ValueError)

    @hide_stdout()
    def test_process_args_latex(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        folder = "test_latex2"
        if not os.path.exists(folder):
            os.mkdir(folder)
        args = Namespace(
            command="latex",
            path=data,
            recursive=False,
            verbose=0,
            output=folder,
        )
        process_args(args)

    def test_process_args_api(self):
        data = os.path.join(os.path.dirname(__file__), "..", "..", "sphinx_runpython")
        folder = "test_api"
        if not os.path.exists(folder):
            os.mkdir(folder)
        args = Namespace(
            command="api",
            path=data,
            recursive=False,
            verbose=0,
            output=folder,
            hidden=False,
        )
        process_args(args)

    def test_process_args_img2pdf(self):
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = os.path.join(tmpdir, "test.png")
            out_path = os.path.join(tmpdir, "out.pdf")
            Image.new("RGB", (100, 100), "white").save(img_path)
            args = Namespace(
                command="img2pdf",
                path=img_path,
                output=out_path,
                verbose=0,
                zoom=1.0,
                rotate=0.0,
            )
            process_args(args)
            self.assertExists(out_path)

    def test_sphinx_api_function(self):
        data = os.path.join(os.path.dirname(__file__), "..", "..", "sphinx_runpython")
        folder = "test_sphinx_api_func"
        if not os.path.exists(folder):
            os.mkdir(folder)
        sphinx_api(data, folder, verbose=0)

    def test_main_latex(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_argv = sys.argv
            try:
                sys.argv = ["sphinx-runpython", "latex", "--path", tmpdir]
                from sphinx_runpython._cmd_helper import main

                main()
            finally:
                sys.argv = old_argv

    def test_main_help(self):
        old_argv = sys.argv
        try:
            sys.argv = ["sphinx-runpython", "--help"]
            from sphinx_runpython._cmd_helper import main

            self.assertRaise(lambda: main(), SystemExit)
        finally:
            sys.argv = old_argv


if __name__ == "__main__":
    unittest.main(verbosity=2)
