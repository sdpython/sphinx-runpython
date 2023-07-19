import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.conf_helper import has_dvipng, has_dvisvgm


class TestHelpers(ExtTestCase):
    def test_dvis(self):
        self.assertIn(has_dvipng(), {True, False})
        self.assertIn(has_dvisvgm(), {True, False})


if __name__ == "__main__":
    unittest.main(verbosity=2)
