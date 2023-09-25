import os
import unittest
from io import StringIO
from contextlib import redirect_stdout
from tempfile import TemporaryDirectory
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.readme import check_readme_syntax


class TestReadme(ExtTestCase):
    def test_venv_docutils08_readme(self):
        fold = os.path.dirname(os.path.abspath(__file__))
        readme = os.path.join(fold, "..", "..", "README.rst")
        assert os.path.exists(readme)
        with open(readme, "r", encoding="utf8") as f:
            content = f.read()
        self.assertNotEmpty(content)

        with TemporaryDirectory() as temp:
            st = StringIO()
            with redirect_stdout(st):
                check_readme_syntax(readme, folder=temp, verbose=1)
            text = st.getvalue()
            print(text)


if __name__ == "__main__":
    unittest.main()
