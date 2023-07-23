import unittest
import os
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython._cmd_helper import get_parser, nb2rst


class TestCmd(ExtTestCase):
    def test_cmd(self):
        parser = get_parser()
        self.assertNotEmpty(parser)

    def test_convert(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        parser = get_parser()
        parser.command = "nb2rst"
        parser.path = data
        nb2rst(data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
