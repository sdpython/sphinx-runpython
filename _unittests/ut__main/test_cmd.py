import platform
import unittest
import os
from sphinx_runpython.ext_test_case import ExtTestCase, hide_stdout
from sphinx_runpython._cmd_helper import get_parser, nb2py, latex_process


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

    #@hide_stdout()
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
