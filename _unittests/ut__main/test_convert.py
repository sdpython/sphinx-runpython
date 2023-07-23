import unittest
import os
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.convert import convert_ipynb_to_gallery


class TestHelpers(ExtTestCase):
    def test_convert_notebook(self):
        data = os.path.join(os.path.dirname(__file__), "data")
        nb = os.path.join(data, "float_and_double_rouding.ipynb")
        res = convert_ipynb_to_gallery(nb)
        self.assertIn("# :math:`\\mathbb{P}", res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
