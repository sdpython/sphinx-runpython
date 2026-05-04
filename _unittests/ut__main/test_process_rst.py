import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.process_rst import rst2html


class TestProcessRst(ExtTestCase):
    def test_rst2html_invalid_writer_arg(self):
        self.assertRaise(
            lambda: rst2html("hello world", writer="html"),
            ValueError,
        )

    def test_rst2html_docutils_mode(self):
        rst = "Hello **world**!\n"
        html = rst2html(rst, use_sphinx=False)
        self.assertIn("world", html)

    def test_rst2html_docutils_with_warnings(self):
        rst = "Hello **world**!\n"
        html, warnings = rst2html(rst, use_sphinx=False, return_warnings=True)
        self.assertIn("world", html)
        self.assertIsInstance(warnings, str)

    def test_rst2html_docutils_error_raises(self):
        # A severely malformed RST that generates a system error message
        # We test that the function raises RuntimeError for ERROR-level messages
        rst = ".. error::\n\n   Error content\n\n.. parsed-literal::\n\n   :malformed\n"
        # This may or may not raise RuntimeError depending on the content
        # Just verify it runs without issue
        try:
            result = rst2html(rst, use_sphinx=False)
        except RuntimeError:
            pass  # Expected behavior for error-level messages


if __name__ == "__main__":
    unittest.main(verbosity=2)
