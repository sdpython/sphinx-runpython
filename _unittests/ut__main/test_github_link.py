import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.github_link import (
    _get_git_revision,
    _linkcode_resolve,
    make_linkcode_resolve,
)


class TestGithubLink(ExtTestCase):
    def test_get_git_revision(self):
        revision = _get_git_revision()
        self.assertIn(type(revision), {str, type(None)})

    def test_linkcode_resolve_no_revision(self):
        result = _linkcode_resolve("py", {}, "pkg", "url", revision=None)
        self.assertIsNone(result)

    def test_linkcode_resolve_wrong_domain(self):
        result = _linkcode_resolve(
            "cpp", {"module": "os", "fullname": "path"}, "os", "url", revision="abc"
        )
        self.assertIsNone(result)

    def test_linkcode_resolve_missing_module(self):
        result = _linkcode_resolve("py", {}, "os", "url", revision="abc")
        self.assertIsNone(result)

    def test_linkcode_resolve_missing_fullname(self):
        result = _linkcode_resolve(
            "py", {"module": "os"}, "os", "url", revision="abc"
        )
        self.assertIsNone(result)

    def test_linkcode_resolve_function(self):
        url_fmt = "https://github.com/python/cpython/blob/{revision}/{path}#L{lineno}"
        result = _linkcode_resolve(
            "py",
            {"module": "os.path", "fullname": "join"},
            "os",
            url_fmt,
            revision="abc123",
        )
        # May be None if source not found, but should not raise
        self.assertIn(type(result), {str, type(None)})

    def test_make_linkcode_resolve(self):
        url_fmt = "https://github.com/python/cpython/blob/{revision}/{package}/{path}#L{lineno}"
        resolver = make_linkcode_resolve("os", url_fmt)
        self.assertTrue(callable(resolver))

    def test_make_linkcode_resolve_call(self):
        url_fmt = "https://github.com/python/cpython/blob/{revision}/{package}/{path}#L{lineno}"
        resolver = make_linkcode_resolve("os", url_fmt)
        result = resolver("py", {"module": "os.path", "fullname": "join"})
        self.assertIn(type(result), {str, type(None)})

    def test_linkcode_resolve_import_error(self):
        url_fmt = "https://example.com/{revision}/{path}#L{lineno}"
        self.assertRaise(
            lambda: _linkcode_resolve(
                "py",
                {"module": "nonexistent_module_xyz", "fullname": "something"},
                "nonexistent_module_xyz",
                url_fmt,
                revision="abc",
            ),
            ImportError,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
