import os
import unittest
from sphinx_runpython.ext_test_case import ExtTestCase, sys_path_append
from sphinx_runpython.import_object_helper import (
    import_object,
    import_any_object,
    import_path,
)


class TestImportObjectHelper(ExtTestCase):
    def test_import_function(self):
        obj, name = import_object("os.path.join", "function")
        self.assertIsNotNone(obj)
        self.assertEqual(name, "join")

    def test_import_class(self):
        obj, name = import_object("os.PathLike", "class")
        self.assertIsNotNone(obj)
        self.assertEqual(name, "PathLike")

    def test_import_class_no_init(self):
        import os

        obj, name = import_object("os.PathLike", "class", use_init=False)
        self.assertIsNotNone(obj)
        self.assertEqual(name, "PathLike")
        self.assertIs(obj, os.PathLike)

    def test_import_function_not_a_function(self):
        self.assertRaise(
            lambda: import_object("os.PathLike", "function"), TypeError
        )

    def test_import_class_not_a_class(self):
        self.assertRaise(
            lambda: import_object("os.path.join", "class"), TypeError
        )

    def test_import_method(self):
        obj, name = import_object("os.PathLike.__fspath__", "method")
        self.assertIsNotNone(obj)
        self.assertEqual(name, "__fspath__")

    def test_import_property(self):
        obj, name = import_object(
            "sphinx_runpython.import_object_helper._Types.prop", "property"
        )
        self.assertIsNotNone(obj)
        self.assertEqual(name, "prop")

    def test_import_staticmethod(self):
        obj, name = import_object(
            "sphinx_runpython.import_object_helper._Types.stat", "staticmethod"
        )
        self.assertIsNotNone(obj)
        self.assertEqual(name, "stat")

    def test_import_unknown_kind(self):
        self.assertRaise(
            lambda: import_object("os.path.join", "unknown_kind"), ValueError
        )

    def test_import_nonexistent_module(self):
        self.assertRaise(
            lambda: import_object("nonexistent_xyz.func", "function"), RuntimeError
        )

    def test_import_property_not_a_class(self):
        self.assertRaise(
            lambda: import_object("os.path.join", "property"), TypeError
        )

    def test_import_staticmethod_not_a_class(self):
        self.assertRaise(
            lambda: import_object("os.path.join", "staticmethod"), TypeError
        )

    def test_import_method_not_a_class(self):
        self.assertRaise(
            lambda: import_object("os.path.join", "method"), TypeError
        )

    def test_import_any_object_function(self):
        obj, name, kind = import_any_object("os.path.join")
        self.assertIsNotNone(obj)
        self.assertEqual(name, "join")
        self.assertIn(kind, ("function", "method", "staticmethod", "property", "class"))

    def test_import_any_object_class(self):
        obj, name, kind = import_any_object("os.PathLike")
        self.assertIsNotNone(obj)
        self.assertEqual(name, "PathLike")
        self.assertEqual(kind, "class")

    def test_import_any_object_not_found(self):
        self.assertRaise(
            lambda: import_any_object("nonexistent_xyz_module.func"), ImportError
        )

    def test_import_path_function(self):
        import os.path

        path = import_path(os.path.join)
        self.assertIsNotNone(path)
        self.assertIn("os", path)

    def test_import_path_with_err_msg(self):
        import os.path

        path = import_path(os.path.join, err_msg="extra error info")
        self.assertIsNotNone(path)

    def test_import_path_class(self):
        path = import_path(os.PathLike, class_name="PathLike")
        self.assertIsNotNone(path)

    def test_import_path_not_found(self):
        # Create an object that is in __main__ and can't be imported from there
        class LocalClass:
            pass

        # class_name not matching __main__ raises RuntimeError
        self.assertRaise(
            lambda: import_path(LocalClass, class_name="LocalClass"), RuntimeError
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
