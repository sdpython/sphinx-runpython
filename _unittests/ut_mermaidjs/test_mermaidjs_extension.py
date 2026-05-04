import unittest
import logging
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import (
    ExtTestCase,
    ignore_warnings,
)


class TestMermaidJsExtension(ExtTestCase):
    def setUp(self):
        logger = logging.getLogger("mermaidjs")
        logger.disabled = True

    @ignore_warnings(PendingDeprecationWarning)
    def test_mermaidjs_inline_rst(self):
        """Inline mermaidjs diagram is round-tripped through the RST writer."""
        content = """
before

.. mermaidjs::

    graph LR
        A --> B --> C

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.mermaidjs"]
        )
        self.assertIn("graph LR", content)
        self.assertIn("A --> B --> C", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mermaidjs_inline_html(self):
        """Inline mermaidjs diagram produces a <pre class="mermaid"> element."""
        content = """
before

.. mermaidjs::

    graph LR
        A --> B

after
"""
        html = rst2html(
            content, writer_name="html", new_extensions=["sphinx_runpython.mermaidjs"]
        )
        self.assertIn('class="mermaid"', html)
        self.assertIn("graph LR", html)
        self.assertIn("A --&gt; B", html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mermaidjs_script(self):
        """Script-generated mermaidjs diagram is included in the RST output."""
        content = """
before

.. mermaidjs::
    :script:

    print(\"\"\"graph LR
    X --> Y\"\"\")

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.mermaidjs"]
        )
        self.assertIn("graph LR", content)
        self.assertIn("X --> Y", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mermaidjs_script_split(self):
        """When :script: has a value it is used as a split token."""
        content = """
before

.. mermaidjs::
    :script: BEGIN

    print("preamble")
    print("BEGIN")
    print("graph TD")
    print("    P --> Q")

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.mermaidjs"]
        )
        self.assertNotIn("preamble", content)
        self.assertNotIn("BEGIN", content)
        self.assertIn("graph TD", content)
        self.assertIn("P --> Q", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_mermaidjs_script_cache(self):
        """Identical scripts produce the same output and are cached."""
        script_body = 'print("graph LR\\n    A --> B")'
        content = f"""
before

.. mermaidjs::
    :script:

    {script_body}

middle

.. mermaidjs::
    :script:

    {script_body}

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.mermaidjs"]
        )
        count = content.count("graph LR")
        self.assertEqual(count, 2, f"Expected diagram code twice, got {count}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
