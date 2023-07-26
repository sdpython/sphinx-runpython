import unittest
import logging
import sys
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase, ignore_warnings


class TestGDotExtension(ExtTestCase):
    def setUp(self):
        logger = logging.getLogger("gdot")
        logger.disabled = True

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot1(self):
        content = """
                    before

                    .. gdot::

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace(
            "                    ", ""
        )

        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn(
            'digraphfoo{"bar"->"baz";}', content.replace("\n", "").replace(" ", "")
        )

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot2(self):
        content = """
                    before

                    .. gdot::
                        :script:

                        print('''digraph foo { HbarH -> HbazH; }'''.replace("H", '"'))

                    after
                    """.replace(
            "                    ", ""
        )

        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn('digraph foo { "bar" -> "baz"; }', content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot2_split(self):
        content = """
            before

            .. gdot::
                :script: BEGIN

                print('''...BEGINdigraph foo { HbarH -> HbazH; }'''.replace("H", '"'))

            after
            """.replace(
            "            ", ""
        )

        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn('digraph foo { "bar" -> "baz"; }', content)
        self.assertNotIn("BEGIN", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot3_svg(self):
        content = """
                    before

                    .. gdot::
                        :format: svg

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace(
            "                    ", ""
        )

        content = rst2html(
            content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn("document.getElementById('gdot-", content)
        self.assertIn('foo {\\n  \\"bar\\" -> \\"baz\\";\\n}");', content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot3_svg_process(self):
        content = """
                    before

                    .. gdot::
                        :format: svg
                        :process:

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace(
            "                    ", ""
        )

        content = rst2html(
            content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn("document.getElementById('gdot-", content)
        self.assertIn('foo {\\n  \\"bar\\" -> \\"baz\\";\\n}");', content)

    @unittest.skipIf(sys.platform != "linux", reason="Missing dependency.")
    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot4_png(self):
        content = """
                    before

                    .. gdot::
                        :format: png

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace(
            "                    ", ""
        )

        try:
            content = rst2html(
                content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
            )
        except FileNotFoundError:
            # This class cannot write on disk.
            return
        self.assertIn("png", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
