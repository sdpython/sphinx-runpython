import os
import unittest
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.runpython.sphinx_runpython_extension import RunPythonDirective


class TestRunPythonStoreInFile(ExtTestCase):
    def test_runpython_store_in_file(self):
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
                        :process:
                        :store_in_file: __DEST__

                        import math
                        import inspect

                        def fctfct():
                            return math.pi

                        code = inspect.getsource(fctfct)
                        print("***********")
                        print(code)
                        print("***********")
                    """.replace(
            "                    ", ""
        )

        temp = os.path.abspath(os.path.dirname(__file__))
        dest = os.path.join(temp, "exescript.py")
        content = content.replace("__DEST__", dest)
        rst = rst2html(content, writer="rst")
        self.assertIn("def fctfct():", rst)
        self.assertIn("return math.pi", rst)
        self.assertExists(dest)


if __name__ == "__main__":
    unittest.main()
