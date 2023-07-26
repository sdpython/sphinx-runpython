import unittest
from docutils.parsers.rst import directives
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings
from sphinx_runpython.blocdefs.sphinx_blocref_extension import (
    BlocRef,
    BlocRefList,
    blocref_node,
    visit_blocref_node,
    depart_blocref_node,
)


class TestBlocRefExtension(ExtTestCase):
    @ignore_warnings(PendingDeprecationWarning)
    def test_post_parse_blocref(self):
        directives.register_directive("blocref", BlocRef)
        directives.register_directive("blocreflist", BlocRefList)

    @ignore_warnings(PendingDeprecationWarning)
    def test_blocref_rst(self):
        content = """
                    test a directive
                    ================

                    before

                    .. blocref::
                        :title: first todo
                        :tag: bug
                        :lid: id3

                        this code should appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            ("blocref", BlocRef, blocref_node, visit_blocref_node, depart_blocref_node)
        ]

        html = rst2html(
            content,
            writer="rst",
            keep_warnings=True,
            directives=tives,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "after"
        if t1 not in html:
            raise Exception(html)

        t1 = "first todo"
        if t1 not in html:
            raise Exception(html)

        if "<SYSTEM MESSAGE" in html:
            raise Exception(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_blocref_html(self):
        content = """
                    test a directive
                    ================

                    before

                    .. blocref::
                        :title: first todo
                        :tag: bug
                        :lid: id3

                        this code should appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            ("blocref", BlocRef, blocref_node, visit_blocref_node, depart_blocref_node)
        ]

        html = rst2html(
            content,
            writer="rst",
            keep_warnings=True,
            directives=tives,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "after"
        if t1 not in html:
            raise Exception(html)

        t1 = "first todo"
        if t1 not in html:
            raise Exception(html)

        if "<SYSTEM MESSAGE" in html:
            raise Exception(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_blocref2(self):
        content = """
                    test a directive
                    ================

                    before

                    .. blocref::
                        :title: first todo
                        :tag: bug
                        :label: id3

                        this code shoud appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            ("blocref", BlocRef, blocref_node, visit_blocref_node, depart_blocref_node)
        ]

        html = rst2html(
            content,
            writer="rst",
            keep_warnings=True,
            directives=tives,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code shoud appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "after"
        if t1 not in html:
            raise Exception(html)

        t1 = "first todo"
        if t1 not in html:
            raise Exception(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_blocreflist(self):
        content = """
                    test a directive
                    ================

                    before

                    .. blocref::
                        :title: first todo
                        :tag: freg
                        :lid: id3

                        this code should appear___

                    middle

                    .. blocreflist::
                        :tag: freg
                        :sort: title
                        :contents: 1

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer="html")

        t1 = "this code should appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "after"
        if t1 not in html:
            raise Exception(html)

        t1 = "first todo"
        if t1 not in html:
            raise Exception(html)


if __name__ == "__main__":
    unittest.main()
