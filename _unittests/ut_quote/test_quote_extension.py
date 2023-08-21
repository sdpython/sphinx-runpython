import unittest
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase


class TestQuoteExtension(ExtTestCase):
    def test_quote(self):
        content = """
                    .. quote::
                        :author: auteur
                        :book: livre titre
                        :lid: label1
                        :pages: 234
                        :year: 2018

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "livre titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "livre titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_manga(self):
        content = """
                    .. quote::
                        :author: auteur
                        :manga: manga titre
                        :lid: label1
                        :pages: 234
                        :year: 2018

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "manga titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "manga titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_film(self):
        content = """
                    .. quote::
                        :author: auteur
                        :film: film titre
                        :lid: label1
                        :pages: 234
                        :year: 2018

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "film titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "film titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_show(self):
        content = """
                    .. quote::
                        :author: auteur
                        :show: show titre
                        :lid: label1
                        :pages: 234
                        :year: 2018
                        :title1: true

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "show titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "show titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_comic(self):
        content = """
                    .. quote::
                        :author: auteur
                        :comic: comic titre
                        :lid: label1
                        :pages: 234
                        :year: 2018
                        :title1: true

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "comic titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "comic titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_disc(self):
        content = """
                    .. quote::
                        :author: auteur
                        :disc: disc titre
                        :lid: label1
                        :pages: 234
                        :year: 2018
                        :title1: true

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "disc titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "disc titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_ado(self):
        content = """
                    .. quote::
                        :author: auteur
                        :ado: ado titre
                        :lid: label1
                        :pages: 234
                        :year: 2018
                        :title1: true

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "ado titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "ado titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)

    def test_quote_child(self):
        content = """
                    .. quote::
                        :author: auteur
                        :child: child titre
                        :lid: label1
                        :pages: 234
                        :year: 2018
                        :title1: true

                        this code should appear___

                    next
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        html = rst2html(
            content,
            writer_name="html",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)
        if "auteur" not in html:
            raise AssertionError(html)
        if "child titre" not in html:
            raise AssertionError(html)
        if "234" not in html:
            raise AssertionError(html)

        rst = rst2html(
            content,
            writer_name="rst",
            keep_warnings=True,
            extlinks={"issue": ("http://%s", "_issue_%s")},
        )

        t1 = "this code should appear"
        if t1 not in rst:
            raise AssertionError(rst)
        if "auteur" not in rst:
            raise AssertionError(rst)
        if "child titre" not in rst:
            raise AssertionError(rst)
        if "234" not in rst:
            raise AssertionError(rst)
        if ".. quote::" not in rst:
            raise AssertionError(rst)
        if ":author: auteur" not in rst:
            raise AssertionError(rst)


if __name__ == "__main__":
    unittest.main()
