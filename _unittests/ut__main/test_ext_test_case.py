import os
import sys
import unittest
import warnings
import numpy
from sphinx_runpython.ext_test_case import (
    ExtTestCase,
    unit_test_going,
    ignore_warnings,
    hide_stdout,
    sys_path_append,
    is_windows,
    is_apple,
    is_linux,
    skipif_ci_windows,
    skipif_ci_linux,
    skipif_ci_apple,
)


class TestExtTestCase(ExtTestCase):
    def test_unit_test_going_default(self):
        old = os.environ.get("UNITTEST_GOING", None)
        try:
            if "UNITTEST_GOING" in os.environ:
                del os.environ["UNITTEST_GOING"]
            result = unit_test_going()
            self.assertFalse(result)
        finally:
            if old is not None:
                os.environ["UNITTEST_GOING"] = old

    def test_unit_test_going_set(self):
        old = os.environ.get("UNITTEST_GOING", None)
        try:
            os.environ["UNITTEST_GOING"] = "1"
            result = unit_test_going()
            self.assertTrue(result)
        finally:
            if old is not None:
                os.environ["UNITTEST_GOING"] = old
            elif "UNITTEST_GOING" in os.environ:
                del os.environ["UNITTEST_GOING"]

    def test_ignore_warnings_none(self):
        def dummy():
            pass

        wrapper = ignore_warnings([UserWarning])
        decorated = wrapper(dummy)
        self.assertTrue(callable(decorated))

    def test_ignore_warnings_warns_none_raises(self):
        self.assertRaise(
            lambda: ignore_warnings(None)(lambda: None)(),
            AssertionError,
        )

    def test_hide_stdout_basic(self):
        @hide_stdout()
        def my_func(self):
            print("hidden output")

        my_func(self)

    def test_hide_stdout_with_callback(self):
        captured = []

        @hide_stdout(lambda s: captured.append(s))
        def my_func(self):
            print("captured text")

        my_func(self)
        self.assertEqual(len(captured), 1)
        self.assertIn("captured text", captured[0])

    def test_sys_path_append_front(self):
        old_path = sys.path.copy()
        test_path = "/tmp/test_path_prepend"
        with sys_path_append([test_path], position=0):
            self.assertIn(test_path, sys.path)
            self.assertEqual(sys.path[0], test_path)
        self.assertEqual(sys.path, old_path)

    def test_sys_path_append_end(self):
        old_path = sys.path.copy()
        test_path = "/tmp/test_path_append"
        with sys_path_append(test_path):
            self.assertIn(test_path, sys.path)
        self.assertEqual(sys.path, old_path)

    def test_is_windows(self):
        self.assertIn(is_windows(), {True, False})

    def test_is_apple(self):
        self.assertIn(is_apple(), {True, False})

    def test_is_linux(self):
        self.assertIn(is_linux(), {True, False})

    def test_platform_skip_decorators(self):
        decorator_win = skipif_ci_windows("test")
        decorator_linux = skipif_ci_linux("test")
        decorator_apple = skipif_ci_apple("test")
        self.assertTrue(callable(decorator_win))
        self.assertTrue(callable(decorator_linux))
        self.assertTrue(callable(decorator_apple))

    def test_assert_exists_passes(self):
        self.assertExists(__file__)

    def test_assert_exists_fails(self):
        self.assertRaise(
            lambda: self.assertExists("/nonexistent/path/file.txt"),
            AssertionError,
        )

    def test_assert_equal_array(self):
        a = numpy.array([1.0, 2.0, 3.0])
        b = numpy.array([1.0, 2.0, 3.0])
        self.assertEqualArray(a, b)

    def test_assert_almost_equal(self):
        a = numpy.array([1.0, 2.0, 3.0])
        b = [1.0, 2.0, 3.0]
        self.assertAlmostEqual(a, b)

    def test_assert_raise_passes(self):
        self.assertRaise(lambda: 1 / 0, ZeroDivisionError)

    def test_assert_raise_wrong_type_propagates(self):
        # When assertRaise is called with wrong exc_type, the exception propagates
        with self.assertRaises(ZeroDivisionError):
            self.assertRaise(lambda: 1 / 0, ValueError)

    def test_assert_raise_no_exception(self):
        self.assertRaise(
            lambda: self.assertRaise(lambda: None, ValueError),
            AssertionError,
        )

    def test_assert_empty_none(self):
        self.assertEmpty(None)

    def test_assert_empty_list(self):
        self.assertEmpty([])

    def test_assert_empty_fails(self):
        self.assertRaise(lambda: self.assertEmpty([1, 2, 3]), AssertionError)

    def test_assert_not_empty_none_fails(self):
        self.assertRaise(lambda: self.assertNotEmpty(None), AssertionError)

    def test_assert_not_empty_empty_list_fails(self):
        self.assertRaise(lambda: self.assertNotEmpty([]), AssertionError)

    def test_assert_not_empty_passes(self):
        self.assertNotEmpty([1, 2])
        self.assertNotEmpty("abc")

    def test_assert_starts_with_passes(self):
        self.assertStartsWith("hello", "hello world")

    def test_assert_starts_with_fails(self):
        self.assertRaise(
            lambda: self.assertStartsWith("world", "hello world"),
            AssertionError,
        )

    def test_capture(self):
        def my_func():
            print("output text")
            return 42

        result, stdout, stderr = self.capture(my_func)
        self.assertEqual(result, 42)
        self.assertIn("output text", stdout)

    def test_teardown_with_warns(self):
        # Test that tearDownClass works with stored warnings
        class TempTestCase(ExtTestCase):
            _warns = []

        TempTestCase.tearDownClass()


if __name__ == "__main__":
    unittest.main(verbosity=2)
