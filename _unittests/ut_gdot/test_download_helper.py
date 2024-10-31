import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.ext_io_helper import get_url_content_timeout, InternetException


class TestDownloadHelper(ExtTestCase):
    def test_download_notimeout(self):
        url = "https://raw.githubusercontent.com/sdpython/pyquickhelper/master/src/pyquickhelper/ipythonhelper/magic_parser.py"
        content = get_url_content_timeout(url, encoding="utf8")
        self.assertIn("MagicCommandParser", content)
        self.assertIsInstance(content, str)

    def test_download_timeout(self):
        url = "https://localhost:878777/should_not_exists"
        try:
            get_url_content_timeout(url, encoding="utf8", timeout=2)
        except InternetException:
            return

        raise AssertionError(f"No exception raised for url={url!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
