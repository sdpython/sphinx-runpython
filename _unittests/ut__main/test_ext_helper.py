import unittest
from docutils import nodes
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.ext_helper import (
    NodeEnter,
    NodeLeave,
    TinyNode,
    WrappedNode,
    traverse,
    sphinx_lang,
)


class TestExtHelper(ExtTestCase):
    def test_tiny_node(self):
        parent = object()
        node = TinyNode(parent)
        self.assertIs(node.parent, parent)

    def test_node_enter(self):
        parent = object()
        node = NodeEnter(parent)
        self.assertIsInstance(node, TinyNode)
        self.assertIs(node.parent, parent)

    def test_node_leave(self):
        parent = object()
        node = NodeLeave(parent)
        self.assertIsInstance(node, TinyNode)
        self.assertIs(node.parent, parent)

    def test_wrapped_node(self):
        doc_node = nodes.section()
        wrapped = WrappedNode(doc_node)
        self.assertIs(wrapped.node, doc_node)

    def test_traverse_simple(self):
        root = nodes.section()
        para = nodes.paragraph(text="hello")
        root += para

        results = list(traverse(root))
        self.assertGreater(len(results), 0)
        depths = [d for d, n in results]
        node_types = [type(n) for d, n in results]
        self.assertIn(0, depths)
        self.assertIn(NodeEnter, node_types)
        self.assertIn(NodeLeave, node_types)
        self.assertIn(nodes.section, node_types)
        self.assertIn(nodes.paragraph, node_types)

    def test_traverse_with_wrapped_node(self):
        root = nodes.paragraph(text="test")
        wrapped = WrappedNode(root)
        results = list(traverse(wrapped))
        self.assertGreater(len(results), 0)
        node_types = [type(n) for d, n in results]
        self.assertIn(NodeEnter, node_types)
        self.assertIn(NodeLeave, node_types)

    def test_traverse_depth(self):
        root = nodes.section()
        child = nodes.paragraph(text="child")
        grandchild = nodes.Text("text")
        child += grandchild
        root += child

        results = list(traverse(root))
        max_depth = max(d for d, n in results)
        self.assertGreaterEqual(max_depth, 2)

    def test_sphinx_lang_no_settings(self):
        class FakeEnv:
            pass

        lang = sphinx_lang(FakeEnv())
        self.assertEqual(lang, "en")

    def test_sphinx_lang_with_settings_no_code(self):
        class FakeSettings:
            pass

        class FakeEnv:
            settings = FakeSettings()

        lang = sphinx_lang(FakeEnv())
        self.assertEqual(lang, "en")

    def test_sphinx_lang_with_language_code(self):
        class FakeSettings:
            language_code = "fr"

        class FakeEnv:
            settings = FakeSettings()

        lang = sphinx_lang(FakeEnv())
        self.assertEqual(lang, "fr")


if __name__ == "__main__":
    unittest.main(verbosity=2)
