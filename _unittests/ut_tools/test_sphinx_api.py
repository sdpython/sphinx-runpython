import os
import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.tools.sphinx_api import sphinx_api


class TestSphinxApi(ExtTestCase):

    def test_this_doc_simulate(self):
        doc = os.path.join(os.path.dirname(__file__), "..", "..", "sphinx_runpython")
        res = sphinx_api(doc, simulate=True, verbose=1)
        self.assertEmpty(res)

    def test_this_doc_write(self):
        doc = os.path.join(os.path.dirname(__file__), "..", "..", "sphinx_runpython")
        output = os.path.join(os.path.dirname(__file__), "temp_this_doc")
        res = sphinx_api(doc, simulate=False, verbose=1, output_folder=output)
        print(res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
