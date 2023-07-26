import unittest
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings


class TestMathDefExtension(ExtTestCase):
    @ignore_warnings(PendingDeprecationWarning)
    def test_mathdef(self):
        content = """
                    test a directive
                    ================

                    before

                    .. mathdef::
                        :title: first def
                        :tag: definition
                        :lid: label1

                        this code should appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="rst",
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "first def"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mathdeflist(self):
        content = """
                    test a directive
                    ================

                    before

                    .. mathdef::
                        :title: first def2
                        :tag: Theoreme

                        this code should appear___

                    middle

                    .. mathdeflist::
                        :tag: definition

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer_name="rst")

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "first def2"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mathdeflist_contents(self):
        content = """
                    test a directive
                    ================

                    before

                    .. mathdef::
                        :title: first def2
                        :tag: Theoreme

                        this code should appear___

                    middle

                    .. mathdeflist::
                        :tag: definition
                        :contents:

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer_name="rst")

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "first def2"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mathdeflist_contents_body_sphinx(self):
        content = """
                    test a directive
                    ================

                    before

                    .. mathdef::
                        :title: first def2
                        :tag: Theoreme

                        this code should appear___

                    middle

                    .. mathdeflist::
                        :tag: definition
                        :contents:

                    middle2

                    .. mathdeflist::
                        :tag: Theoreme
                        :contents:

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="rst",
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)

        t1 = "first def2"
        if t1 not in html:
            raise AssertionError("ISSUE in \n" + html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
