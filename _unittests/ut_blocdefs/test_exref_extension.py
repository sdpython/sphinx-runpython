import unittest
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings


class TestExRefExtension(ExtTestCase):
    @ignore_warnings(PendingDeprecationWarning)
    def test_exref(self):
        content = """
                    test a directive
                    ================

                    before

                    .. exref::
                        :title: first todo
                        :tag: bug
                        :lid: id3

                        this code shoud appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="rst",
        )

        t1 = "this code shoud appear"
        if t1 not in html:
            raise AssertionError("ISSUE in " + html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError("ISSUE in " + html)

        t1 = "first todo"
        if t1 not in html:
            raise AssertionError("ISSUE in " + html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_exreflist(self):
        content = """
                    test a directive
                    ================

                    before

                    .. exref::
                        :title: first todo
                        :tag: freg
                        :lid: id3

                        this code shoud appear___

                    middle

                    .. exreflist::
                        :tag: freg
                        :sort: title

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(content, writer_name="rst")

        t1 = "this code shoud appear"
        if t1 not in html:
            raise AssertionError("ISSUE in " + html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError("ISSUE in " + html)

        t1 = "first todo"
        if t1 not in html:
            raise AssertionError("ISSUE in " + html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_exreflist_rst(self):
        content = """
                    test a directive
                    ================

                    before

                    .. exref::
                        :title: first todo
                        :tag: freg
                        :lid: id3

                        this code shoud appear___

                    middle

                    .. exreflist::
                        :tag: freg
                        :sort: title

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        rst = rst2html(content, writer_name="rst")

        self.assertNotEmpty(rst)


if __name__ == "__main__":
    unittest.main(verbosity=2)
