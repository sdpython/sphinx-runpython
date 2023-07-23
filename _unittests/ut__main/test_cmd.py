import unittest
import os
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython._cmd_helper import get_parser, nb2py


class TestCmd(ExtTestCase):
    def test_cmd(self):
        parser = get_parser()
        self.assertNotEmpty(parser)

    def test_convert(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        parser = get_parser()
        parser.command = "nb2py"
        parser.path = data
        nb2py(data, verbose=1)
        expected = os.path.join(data, "float_and_double_rouding.py")
        self.assertExists(expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
