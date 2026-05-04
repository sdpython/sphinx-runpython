import unittest
from unittest.mock import patch
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.conf_helper import has_dvipng, has_dvisvgm, _check_cmd


class TestHelpers(ExtTestCase):
    def test_dvis(self):
        self.assertIn(has_dvipng(), {True, False})
        self.assertIn(has_dvisvgm(), {True, False})

    def test_check_cmd_found(self):
        with patch("sphinx_runpython.conf_helper.run_cmd") as mock_run:
            mock_run.return_value = ("dvipng version 1.0", "")
            result = _check_cmd("dvipng")
            self.assertTrue(result)

    def test_check_cmd_not_found_in_output(self):
        with patch("sphinx_runpython.conf_helper.run_cmd") as mock_run:
            mock_run.return_value = ("some other output", "")
            result = _check_cmd("dvipng")
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
