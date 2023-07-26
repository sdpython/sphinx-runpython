import unittest
from sphinx_runpython.helpers import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.runpython.sphinx_runpython_extension import (
    RunPythonDirective,
    runpython_node,
    visit_runpython_node,
    depart_runpython_node,
)

tives = [
    (
        "runpython",
        RunPythonDirective,
        runpython_node,
        visit_runpython_node,
        depart_runpython_node,
    )
]


class TestRunPythonCodeBlock(ExtTestCase):
    def test_code_block(self):
        content = """
                    .. code-block:: csharp

                        ens = ["f", 0]
                        for j in ens:
                            print(j)
                    """.replace(
            "                    ", ""
        )

        rst = rst2html(content, writer="doctree", keep_warnings=True, directives=tives)
        self.assertIn("csharp", str(rst))

    def test_runpython_csharp(self):
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.add_text("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.add_text("<p><b>depart_rp_node</b></p>")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :rst:
                        :showcode:
                        :language: csharp
                        :exception:

                        int f(double x)
                        {
                            return x.ToInt();
                        }
                    """.replace(
            "                    ", ""
        )

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        rst = rst2html(content, writer="rst", keep_warnings=True, directives=tives)
        self.assertIn(".. code-block:: csharp", rst)


if __name__ == "__main__":
    unittest.main()
