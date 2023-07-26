import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.import_object_helper import import_object
from sphinx_runpython.docassert.sphinx_docassert_extension import parse_signature


class TestDocAssertCpp(ExtTestCase):
    def test_import_objec1(self):
        name = "onnx_extended.ortcy.wrap.ortinf.OrtSession"
        try:
            obj, new_name = import_object(name, kind="class")
        except ImportError:
            return
        self.assertEqual(name.split(".")[-1], new_name)
        self.assertEqual(obj.__text_signature__, "($self, /, *args, **kwargs)")

    def test_import_objec2(self):
        name = "onnx_extended.validation.cpu._validation.benchmark_cache"
        try:
            obj, new_name = import_object(name, kind="function")
        except ImportError:
            return
        self.assertEqual(name.split(".")[-1], new_name)
        self.assertEmpty(obj.__text_signature__)
        sig = parse_signature(obj.__doc__)
        self.assertEqual(
            repr(sig), "benchmark_cache(size: int, verbose: bool = True) -> float"
        )
        self.assertIn("size", sig.param_names)

    def test_extract_signature(self):
        sig = (
            "benchmark_cache(size: int, verbose: bool = True) -> float\n\n "
            "Runs a benchmark to measure the cache performance.\nThe function "
            "measures the time for N random accesses in array of size N\nand "
            "returns the time divided by N.\nIt copies random elements taken "
            "from the array size to random\nposition in another of the same size. "
            "It does that *size* times\nand return the average time per move."
            "\nSee example :ref:`l-example-bench-cpu`.\n\n"
            ":param size: array size\n:return: average time per move\n\n'"
        )
        res = parse_signature(sig)
        self.assertEqual(
            repr(res), "benchmark_cache(size: int, verbose: bool = True) -> float"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
