import unittest
from sphinx_runpython.process_rst import rst2html
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

        rst = rst2html(content, writer_name="rst")
        self.assertIn("csharp", str(rst))

    def test_runpython_csharp(self):
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        content = """
                    test a directive
                    ================

                    .. runpython::
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

        rst = rst2html(content, writer_name="rst")
        self.assertIn(".. code-block:: csharp", rst)


if __name__ == "__main__":
    unittest.main()
