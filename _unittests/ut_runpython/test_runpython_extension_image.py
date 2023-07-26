import sys
import os
import unittest
from docutils.parsers.rst import directives
from sphinx_runpython.helpers import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.runpython.sphinx_runpython_extension import RunPythonDirective


class TestRunPythonExtensionImage(ExtTestCase):
    def test_post_parse(self):
        directives.register_directive("runpython", RunPythonDirective)

    def test_runpython_image(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        temp = os.path.abspath(os.path.dirname(__file__))
        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :rst:
                        :showcode:

                        import matplotlib.pyplot as plt
                        fig, ax = plt.subplots(1, 1, figsize=(4, 4))
                        ax.plot([0, 1], [0, 1], '--')
                        if __WD__ is None:
                            raise AssertionError(__WD__)
                        fig.savefig("__FOLD__/oo.png")

                        text = ".. image:: oo.png\\n    :width: 200px"
                        print(text)

                    """.replace(
            "                    ", ""
        ).replace(
            "__FOLD__", temp.replace("\\", "/")
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        with open(os.path.join(temp, "out.html"), "w", encoding="utf8") as f:
            f.write(html)
        img = os.path.join(temp, "oo.png")
        self.assertExists(img)


if __name__ == "__main__":
    unittest.main()
