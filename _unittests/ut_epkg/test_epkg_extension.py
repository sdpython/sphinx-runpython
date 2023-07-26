import unittest
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.epkg.sphinx_epkg_extension import (
    epkg_role,
    epkg_node,
    visit_epkg_node,
    depart_epkg_node,
)


tives = [("epkg", epkg_role, epkg_node, visit_epkg_node, depart_epkg_node)]


class TestEpkgExtension(ExtTestCase):
    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_module(self):
        content = """
                    test a directive
                    ================

                    abeforea :epkg:`pandas` aaftera
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="rst",
        )

        t1 = "abeforea"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "aftera"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "https://pandas.pydata.org/pandas-docs/stable/"
        if t1 not in html:
            raise AssertionError(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_module_twice(self):
        content = """
                    abeforea :epkg:`pandas` aaftera

                    test a directive
                    ================

                    abeforea :epkg:`pandas` aaftera
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="rst",
        )
        self.assertIn("https://pandas.pydata.org/pandas-docs/stable/", html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_sub(self):
        content = """
                    test a directive
                    ================

                    abeforea :epkg:`pandas:DataFrame.to_html` aaftera
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer_name="html")

        t1 = "abeforea"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "aftera"
        if t1 not in html:
            raise AssertionError(html)

        spl = html.split("abeforea")[-1].split("aftera")[0]

        t1 = "`"
        if t1 in html:
            raise AssertionError(f"\n**{spl}**\n----\n{html}")

    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_function(self):
        content = """
                    test a directive
                    ================

                    abeforea :epkg:`pandas:DataFrame:to_html` aaftera
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        def pandas_link(input):
            return "MYA", "|".join(input.split(":"))

        html = rst2html(content, writer_name="html")

        t1 = "abeforea"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "aftera"
        if t1 not in html:
            raise AssertionError(html)

        spl = html.split("abeforea")[-1].split("aftera")[0]

        t1 = "`"
        if t1 in html:
            raise AssertionError(f"\n**{spl}**\n----\n{html}")

        t1 = "https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html"
        if t1 not in html:
            raise AssertionError(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_class(self):
        content = """
                    test a directive
                    ================

                    abeforea :epkg:`pandas:DataFrame:to_html` aaftera

                    7za :epkg:`Pandoc` 7zb
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        class pandas_link:
            def __call__(self, input):
                return "MYA", "|".join(input.split(":"))

        html = rst2html(content, writer_name="html")

        self.assertIn("abeforea", html)
        self.assertIn("aftera", html)

        self.assertNotIn("`", html)
        self.assertIn('https://johnmacfarlane.net/pandoc/"', html)
        self.assertIn(
            "https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html",
            html,
        )

    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_function_string(self):
        content = """
                    test a directive
                    ================

                    abeforea :epkg:`pandas:DataFrame:to_html` aaftera
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer_name="html")

        t1 = "abeforea"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "aftera"
        if t1 not in html:
            raise AssertionError(html)

        spl = html.split("abeforea")[-1].split("aftera")[0]

        t1 = "`"
        if t1 in html:
            raise AssertionError(f"\n**{spl}**\n----\n{html}")

        t1 = "https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html"
        if t1 not in html:
            raise AssertionError(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_epkg_function_long_link(self):
        content = """
                    test a directive
                    ================

                    `one link on two lines <http://first.part/
                    second part>`_.
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer_name="html")

        t1 = 'href="http://first.part/secondpart"'
        if t1 not in html:
            raise AssertionError(html)

        t1 = ">one link on two lines</a>"
        if t1 not in html:
            raise AssertionError(html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
