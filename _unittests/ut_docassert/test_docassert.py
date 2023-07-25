"""
@brief      test log(time=8s)
@author     Xavier Dupre
"""
import os
from io import StringIO
import unittest
import warnings
import logging
from sphinx.util.logging import getLogger
from pyquickhelper.helpgen import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, sys_path_append, ignore_warnings
from sphinx_runpython.import_object_helper import import_object
from sphinx_runpython.docassert.sphinx_docassert_extension import parse_signature


class TestDocAssert(ExtTestCase):
    def test_import_object(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("exdocassert.onefunction", "function")
            self.assertTrue(obj is not None)
            self.assertTrue(obj(4, 5), 9)

    @ignore_warnings(PendingDeprecationWarning)
    def test_docassert_html(self):
        logger1 = getLogger("MockSphinxApp")
        logger2 = getLogger("docassert")

        log_capture_string = StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger1.logger.addHandler(ch)
        logger2.logger.addHandler(ch)

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("exdocassert.onefunction", "function")
            docstring = obj.__doc__
            with warnings.catch_warnings(record=True) as ws:
                html = rst2html(docstring)
                if "if a and b have different" not in html:
                    raise AssertionError(html)

            newstring = ".. autofunction:: exdocassert.onefunction"
            with warnings.catch_warnings(record=True) as ws:
                html = rst2html(newstring)
                if "if a and b have different" not in html:
                    html = [rst2html(newstring)]
                    html.append(f"number of warnings {len(ws)}")
                    for i, w in enumerate(ws):
                        html.append(f"{i}: {w}")
                    raise AssertionError(html)

            from docutils.parsers.rst.directives import _directives

            self.assertTrue("autofunction" in _directives)

        lines = log_capture_string.getvalue().split("\n")
        if len(lines) > 0:
            for line in lines:
                if "'onefunction' has no parameter 'TypeError'" in line:
                    raise AssertionError(
                        "This warning should not happen.\n{0}".format("\n".join(lines))
                    )
        self.assertTrue("<strong>a</strong>" in html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_docassert_html_bug(self):
        class MyStream:
            def __init__(self):
                self.rows = []

            def write(self, text):
                # print("[warning*] {0} - '{1}'".format(len(self), text.strip("\n\r ")))
                self.rows.append(text)

            def getvalue(self):
                return "\n".join(self.rows)

            def __len__(self):
                return len(self.rows)

        logger1 = getLogger("MockSphinxApp")
        logger2 = getLogger("docassert")
        log_capture_string = MyStream()  # StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger1.logger.addHandler(ch)
        logger2.logger.addHandler(ch)
        logger2.warning("try")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("exdocassert2.onefunction", "function")
            newstring = ".. autofunction:: exdocassert2.onefunction"
            html = rst2html(newstring)
            self.assertTrue(html is not None)

        lines = log_capture_string.getvalue().split("\n")
        if len(lines) == 0:
            raise AssertionError("no warning")
        nb = 0
        for line in lines:
            if "'onefunction' has no parameter 'c'" in line:
                nb += 1
        if nb == 0:
            raise AssertionError("not the right warning")

    @ignore_warnings(PendingDeprecationWarning)
    def test_docassert_html_method(self):
        class MyStream:
            def __init__(self):
                self.rows = []

            def write(self, text):
                # print("[warning*] {0} - '{1}'".format(len(self), text.strip("\n\r ")))
                self.rows.append(text)

            def getvalue(self):
                return "\n".join(self.rows)

            def __len__(self):
                return len(self.rows)

        logger1 = getLogger("MockSphinxApp")
        logger2 = getLogger("docassert")
        log_capture_string = MyStream()  # StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger1.logger.addHandler(ch)
        logger2.logger.addHandler(ch)
        logger2.warning("try")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("exsig.clex.onemethod", "method")
            newstring = ".. automethod:: exsig.clex.onemethod"
            html = rst2html(newstring)
            self.assertTrue(html is not None)

        lines = log_capture_string.getvalue().split("\n")
        if len(lines) == 0:
            raise AssertionError("no warning")
        nb = 0
        for line in lines:
            if "'onemethod' has no parameter 'c'" in line:
                nb += 1
        if nb == 0:
            raise AssertionError("not the right warning")
        for line in lines:
            if "'onemethod' has undocumented parameters 'b, self'" in line:
                raise AssertionError(line)

    @ignore_warnings(PendingDeprecationWarning)
    def test_docassert_html_init(self):
        class MyStream:
            def __init__(self):
                self.rows = []

            def write(self, text):
                self.rows.append(text)

            def getvalue(self):
                return "\n".join(self.rows)

            def __len__(self):
                return len(self.rows)

        logger1 = getLogger("MockSphinxApp")
        logger2 = getLogger("docassert")
        log_capture_string = MyStream()  # StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger1.logger.addHandler(ch)
        logger2.logger.addHandler(ch)
        logger2.warning("try")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("clsslk.Estimator", "class")
            newstring = ".. autoclass:: clsslk.Estimator"
            html = rst2html(newstring)
            self.assertTrue(html is not None)

        lines = log_capture_string.getvalue().split("\n")
        if len(lines) == 0:
            raise AssertionError("no warning")
        nb = 0
        for line in lines:
            if "'Estimator' has no parameter 'alph'" in line:
                nb += 1
            if "'Estimator' has undocumented parameters" in line:
                nb += 1
        if nb == 0:
            raise AssertionError("not the right warning")

    @ignore_warnings(PendingDeprecationWarning)
    def test_docassert_html_init2(self):
        class MyStream:
            def __init__(self):
                self.rows = []

            def write(self, text):
                self.rows.append(text)

            def getvalue(self):
                return "\n".join(self.rows)

            def __len__(self):
                return len(self.rows)

        logger1 = getLogger("MockSphinxApp")
        logger2 = getLogger("docassert")
        log_capture_string = MyStream()  # StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger1.logger.addHandler(ch)
        logger2.logger.addHandler(ch)
        logger2.warning("try")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("clsslk.Estimator2", "class")
            newstring = ".. autoclass:: clsslk.Estimator2"
            html = rst2html(newstring, autoclass_content="both")
            self.assertTrue(html is not None)

        lines = log_capture_string.getvalue().split("\n")
        if len(lines) == 0:
            raise AssertionError("no warning")
        nb = 0
        for line in lines:
            if "'Estimator2' has no parameter 'alp'" in line:
                nb += 1
            if "'Estimator2' has undocumented parameters" in line:
                nb += 1
        if nb == 0:
            raise AssertionError("not the right warning")

    @ignore_warnings(PendingDeprecationWarning)
    def test_docassert_html_style(self):
        class MyStream:
            def __init__(self):
                self.rows = []

            def write(self, text):
                self.rows.append(text)

            def getvalue(self):
                return "\n".join(self.rows)

            def __len__(self):
                return len(self.rows)

        logger1 = getLogger("MockSphinxApp")
        logger2 = getLogger("docassert")
        log_capture_string = MyStream()  # StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger1.logger.addHandler(ch)
        logger2.logger.addHandler(ch)
        logger2.warning("try")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "datadoc")
        with sys_path_append(data):
            obj, name = import_object("clsslk.Estimator3", "class")
            newstring = ".. autoclass:: clsslk.Estimator3"
            html = rst2html(
                newstring, autoclass_content="both", new_extensions=["numpydoc"]
            )
            self.assertTrue(html is not None)

        lines = log_capture_string.getvalue().split("\n")
        if len(lines) == 0:
            raise AssertionError("no warning")
        nb = 0
        for line in lines:
            if "'Estimator3' has no parameter 'fit_intercep'" in line:
                nb += 1
            if "'Estimator3' has undocumented parameters 'fit" in line:
                nb += 1
        if nb == 0:
            raise AssertionError("not the right warning")

    def test_extract_signature(self):
        sig = (
            "benchmark_cache(size: int, verbose: bool = True) -> float\n\n "
            "Runs a benchmark to measure the cache performance.\nThe function "
            "measures the time for N random accesses in array of size N\nand "
            "returns the time divided by N.\nIt copies random elements taken "
            "from the array size to random\nposition in another of the same size. "
            "It does that *size* times\nand return the average time per move."
            "\nSee example :ref:`l-example-bench-cpu`.\n\n"
            ":param size: array size\n:return: average time per move\n\n'"
        )
        res = parse_signature(sig)
        self.assertEqual(
            repr(res), "benchmark_cache(size: int, verbose: bool = True) -> float"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
