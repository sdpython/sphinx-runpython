import sys
import unittest
from docutils.parsers.rst import directives
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings
from sphinx_runpython.runpython.sphinx_runpython_extension import RunPythonDirective


class TestRunPythonExtensionToggle(ExtTestCase):
    def test_post_parse(self):
        directives.register_directive("runpython", RunPythonDirective)

    @ignore_warnings(PendingDeprecationWarning)
    def test_runpython_toggle(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            if hasattr(self, "body"):
                self.body.append("<p><b>visit_rp_node</b></p>")
            else:
                self.add_text(".. beginrunpython." + self.nl)

        def depart_rp_node(self, node):
            "local function"
            if hasattr(self, "body"):
                self.body.append("<p><b>depart_rp_node</b></p>")
            else:
                self.add_text(".. endrunpython." + self.nl)

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case should not be")

        content = """
                    test a directive
                    ================

                    .. runpython::
                        :setsysvar:
                        :rst:
                        :showcode:
                        :toggle: both

                        print(u"this code should appear" + u"___")
                        import sys
                        print(u"setsysvar: " + str(
                            sys.__dict__.get(
                                'enable_disabled_documented_pieces_of_code', None)))
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        # HTML
        html = rst2html(content, writer_name="html")

        t1 = "button"
        if t1 not in html:
            raise AssertionError(html)

        # RST
        html = rst2html(content, writer_name="rst")

        t1 = "<<<::"
        t2 = "<<<.. code-block:: python"
        if t1 not in html and t2 not in html:
            raise AssertionError(html)
        t1 = ".. collapse::"
        if t1 not in html:
            raise AssertionError(html)


if __name__ == "__main__":
    unittest.main()
