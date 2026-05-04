import unittest
import logging
from sphinx_runpython.process_rst import rst2html
from sphinx_runpython.ext_test_case import (
    ExtTestCase,
    ignore_warnings,
)


class TestRunMermaidExtension(ExtTestCase):
    def setUp(self):
        logger = logging.getLogger("runmermaid")
        logger.disabled = True

    @ignore_warnings(PendingDeprecationWarning)
    def test_runmermaid_inline_rst(self):
        """Inline runmermaid diagram is round-tripped through the RST writer."""
        content = """
before

.. runmermaid::

    graph LR
        A --> B --> C

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.runmermaid"]
        )
        self.assertIn("graph LR", content)
        self.assertIn("A --> B --> C", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_runmermaid_inline_html(self):
        """Inline runmermaid diagram produces a <pre class="mermaid"> element."""
        content = """
before

.. runmermaid::

    graph LR
        A --> B

after
"""
        html = rst2html(
            content, writer_name="html", new_extensions=["sphinx_runpython.runmermaid"]
        )
        self.assertIn('class="mermaid"', html)
        self.assertIn("graph LR", html)
        self.assertIn("A --&gt; B", html)

    @ignore_warnings(PendingDeprecationWarning)
    def test_runmermaid_script(self):
        """Script-generated runmermaid diagram is included in the RST output."""
        content = """
before

.. runmermaid::
    :script:

    print(\"\"\"graph LR
    X --> Y\"\"\")

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.runmermaid"]
        )
        self.assertIn("graph LR", content)
        self.assertIn("X --> Y", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_runmermaid_script_split(self):
        """When :script: has a value it is used as a split token."""
        content = """
before

.. runmermaid::
    :script: BEGIN

    print("preamble")
    print("BEGIN")
    print("graph TD")
    print("    P --> Q")

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.runmermaid"]
        )
        self.assertNotIn("preamble", content)
        self.assertNotIn("BEGIN", content)
        self.assertIn("graph TD", content)
        self.assertIn("P --> Q", content)

    @ignore_warnings(PendingDeprecationWarning)
    def test_runmermaid_script_cache(self):
        """Identical scripts produce the same output and are cached."""
        script_body = 'print("graph LR\\n    A --> B")'
        content = f"""
before

.. runmermaid::
    :script:

    {script_body}

middle

.. runmermaid::
    :script:

    {script_body}

after
"""
        content = rst2html(
            content, writer_name="rst", new_extensions=["sphinx_runpython.runmermaid"]
        )
        count = content.count("graph LR")
        self.assertEqual(count, 2, f"Expected diagram code twice, got {count}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
