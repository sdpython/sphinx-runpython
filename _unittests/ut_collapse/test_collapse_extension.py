import unittest
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings
from sphinx_runpython.collapse.sphinx_collapse_extension import (
    CollapseDirective,
    collapse_node,
    visit_collapse_node_html,
    depart_collapse_node_html,
    visit_collapse_node_rst,
    depart_collapse_node_rst,
)

tives = [
    (
        "collapse",
        CollapseDirective,
        collapse_node,
        visit_collapse_node_rst,
        depart_collapse_node_rst,
    )
]

tives_html = [
    (
        "collapse",
        CollapseDirective,
        collapse_node,
        visit_collapse_node_html,
        depart_collapse_node_html,
    )
]


class TestCollapseExtension(ExtTestCase):
    @ignore_warnings(PendingDeprecationWarning)
    def test_collapse(self):
        content = """
                    before

                    .. collapse::

                        this code should appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        # RST
        html = rst2html(content, writer_name="rst")

        t1 = "  this code should appear___"
        if t1 not in html:
            raise AssertionError(html)

        t1 = ".. collapse::"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "    :legend:"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError(html)

        t1 = ".. collapse::     :legend:"
        if t1 in html:
            raise AssertionError(html)

        html = rst2html(content, writer_name="rst")

        t1 = "this code should appear"
        if t1 not in html:
            raise AssertionError(html)

        t1 = "after"
        if t1 not in html:
            raise AssertionError(html)

        html = rst2html(content, writer_name="html")

        t1 = 'if (x.style.display === "none")'
        if t1 not in html:
            raise AssertionError(html)

        t1 = "b.innerText = 'unhide';"
        if t1 not in html:
            raise AssertionError(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_collapse_legend(self):
        content = """
                    before

                    .. collapse::
                        :legend: ABC/abcd

                        this code should appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        # RST
        html = rst2html(content, writer_name="rst")

        t1 = ":legend: ABC/abcd"
        if t1 not in html:
            raise AssertionError(html)

        t1 = ":hide:"
        if t1 in html:
            raise AssertionError(html)

        # HTML
        html = rst2html(content, writer_name="html")

        t1 = "b.innerText = 'abcd';"
        if t1 not in html:
            raise AssertionError(html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_collapse_show(self):
        content = """
                    before

                    .. collapse::
                        :legend: ABC/abcd
                        :hide:

                        this code should appear___

                    after
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        # RST
        html = rst2html(content, writer_name="rst")

        t1 = ":hide:"
        if t1 not in html:
            raise AssertionError(html)

        # HTML
        html = rst2html(content, writer_name="html")

        t1 = ">abcd<"
        if t1 not in html:
            raise AssertionError(html)

        t1 = '"display:none;"'
        if t1 not in html:
            raise AssertionError(html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
