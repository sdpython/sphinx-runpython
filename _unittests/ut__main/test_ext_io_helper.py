import os
import unittest
import tempfile
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.ext_io_helper import (
    _get_file_url,
    ReadUrlException,
    InternetException,
    FileException,
    MONTH_DATE,
    get_url_content_timeout,
)


class TestExtIoHelper(ExtTestCase):
    def test_month_date_keys(self):
        self.assertEqual(MONTH_DATE["jan"], 1)
        self.assertEqual(MONTH_DATE["dec"], 12)
        self.assertEqual(len(MONTH_DATE), 12)

    def test_get_file_url_basic(self):
        result = _get_file_url("http://example.com/file.html", "/tmp/cache")
        self.assertIn("/tmp/cache", result)
        self.assertIn("example", result)

    def test_get_file_url_png(self):
        result = _get_file_url("http://example.com/image.png", "/tmp/cache")
        self.assertTrue(result.endswith(".png"))

    def test_get_file_url_no_extension(self):
        result = _get_file_url("http://example.com/noext", "/tmp/cache")
        self.assertIn("/tmp/cache", result)

    def test_get_file_url_query_params(self):
        result = _get_file_url("http://example.com/file?key=value.pdf", "/tmp/cache")
        self.assertIn("/tmp/cache", result)

    def test_get_file_url_py(self):
        result = _get_file_url("http://example.com/script.py", "/tmp/cache")
        self.assertTrue(result.endswith(".py"))

    def test_read_url_exception_custom(self):
        exc = ReadUrlException("test error")
        self.assertIsInstance(exc, Exception)

    def test_internet_exception_custom(self):
        exc = InternetException("test error")
        self.assertIsInstance(exc, Exception)

    def test_file_exception_custom(self):
        exc = FileException("test error")
        self.assertIsInstance(exc, Exception)

    def test_get_url_content_timeout_invalid_url(self):
        url = "https://localhost:87777/nonexistent"
        result = get_url_content_timeout(
            url, timeout=2, raise_exception=False, encoding="utf-8"
        )
        self.assertIsNone(result)

    def test_get_url_content_timeout_raises(self):
        url = "https://localhost:87777/nonexistent"
        self.assertRaise(
            lambda: get_url_content_timeout(url, timeout=2, raise_exception=True),
            InternetException,
        )

    def test_get_url_content_timeout_save_to_file(self):
        url = "https://localhost:87777/nonexistent"
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            outfile = f.name
        try:
            result = get_url_content_timeout(
                url,
                timeout=2,
                output=outfile,
                raise_exception=False,
                encoding="utf-8",
            )
            self.assertIsNone(result)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)


if __name__ == "__main__":
    unittest.main(verbosity=2)
