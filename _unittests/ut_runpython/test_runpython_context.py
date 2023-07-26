import unittest
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.runpython.sphinx_runpython_extension import RunPythonDirective


class TestRunPythoncontext(ExtTestCase):
    def test_runpython_context(self):
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

                    .. runpython::
                        :showcode:
                        :store:

                        magic_store = "saved for later"

                    .. runpython::
                        :restore:

                        a = 5
                        try:
                            print("restored", magic_store)
                        except Exception as e:
                            print("failed")
                            for k, v in sorted(locals().copy().items()):
                                print(k, "=", [v])
                    """.replace(
            "                    ", ""
        )

        rst = rst2html(content, writer="rst")
        self.assertIn("restored saved for later", rst)
        self.assertNotIn("failed", rst)


if __name__ == "__main__":
    unittest.main()
