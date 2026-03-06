import unittest
import logging
import os
import sys
from contextlib import contextmanager
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import (
    ExtTestCase,
    ignore_warnings,
    skipif_ci_apple,
    skipif_ci_windows,
)


@contextmanager
def unittest_going():
    """Context manager that sets UNITTEST_GOING=1 for the duration of the block."""
    old = os.environ.get("UNITTEST_GOING", None)
    os.environ["UNITTEST_GOING"] = "1"
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("UNITTEST_GOING", None)
        else:
            os.environ["UNITTEST_GOING"] = old


class TestGDotExtension(ExtTestCase):
    def setUp(self):
        logger = logging.getLogger("gdot")
        logger.disabled = True

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot1(self):
        content = """
                    before

                    .. gdot::
                        :format: png

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace("                    ", "")

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
                        :format: png

                        print('''digraph foo { HbarH -> HbazH; }'''.replace("H", '"'))

                    after
                    """.replace("                    ", "")

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
                :format: png

                print('''...BEGINdigraph foo { HbarH -> HbazH; }'''.replace("H", '"'))

            after
            """.replace("            ", "")

        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertNotIn("svg", content)
        self.assertNotIn("BEGIN", content)
        self.assertIn("png", content)

    @ignore_warnings(PendingDeprecationWarning)
    @skipif_ci_windows("crash")
    @skipif_ci_apple("crash")
    def test_gdot3_svg(self):
        content = """
                    before

                    .. gdot::
                        :format: svg

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace("                    ", "")

        content = rst2html(
            content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn("svg", content)
        self.assertNotIn("png", content)

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
                    """.replace("                    ", "")

        content = rst2html(
            content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
        )
        self.assertIn("digraph foo {", content)

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
                    """.replace("                    ", "")

        try:
            content = rst2html(
                content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
            )
        except FileNotFoundError:
            # This class cannot write on disk.
            return
        self.assertIn("png", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot_unittest_going_svg(self):
        """When UNITTEST_GOING=1, a dummy SVG containing 'DISABLED FOR TESTS' is rendered."""
        content = """
                    before

                    .. gdot::
                        :format: svg

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace("                    ", "")

        with unittest_going():
            html = rst2html(
                content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
            )

        self.assertIn("DISABLED FOR TESTS", html)
        self.assertIn("<svg", html)
        self.assertNotIn("<img", html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_gdot_unittest_going_png(self):
        """
        When UNITTEST_GOING=1, a dummy image containing
        'DISABLED FOR TESTS' is rendered.
        """
        content = """
                    before

                    .. gdot::
                        :format: png

                        digraph foo {
                          "bar" -> "baz";
                        }

                    after
                    """.replace("                    ", "")

        with unittest_going():
            html = rst2html(
                content, writer_name="html", new_extensions=["sphinx_runpython.gdot"]
            )

        self.assertIn("DISABLED FOR TESTS", html)
        self.assertIn("<img", html)
        self.assertNotIn("<svg", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
