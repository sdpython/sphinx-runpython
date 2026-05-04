import io
import os
import tempfile
import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.tools.img_export import images2pdf


class TestImgExport(ExtTestCase):

    def test_export1(self):
        dest = "test_export1.pdf"
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        datap = os.path.join(os.path.dirname(__file__), "data", "*.jpg")
        res = images2pdf([data, datap], dest)
        self.assertExists(dest)
        self.assertEqual(len(res), 3)

    def test_export2(self):
        dest = "test_export2.pdf"
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        datap = os.path.join(os.path.dirname(__file__), "data", "*.jpg")
        res = images2pdf(",".join([data, datap]), dest)
        self.assertExists(dest)
        self.assertEqual(len(res), 3)

    def test_export_zoom(self):
        dest = "test_export_zoom.pdf"
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        datap = os.path.join(os.path.dirname(__file__), "data", "*.jpg")
        res = images2pdf(",".join([data, datap]), dest, zoom=0.5)
        self.assertExists(dest)
        self.assertEqual(len(res), 3)

    def test_export_single_file_string(self):
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            dest = f.name
        try:
            res = images2pdf(data, dest)
            self.assertExists(dest)
            self.assertEqual(len(res), 1)
        finally:
            if os.path.exists(dest):
                os.remove(dest)

    def test_export_glob_string(self):
        datap = os.path.join(os.path.dirname(__file__), "data", "*.jpg")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            dest = f.name
        try:
            res = images2pdf(datap, dest)
            self.assertExists(dest)
            self.assertGreater(len(res), 0)
        finally:
            if os.path.exists(dest):
                os.remove(dest)

    def test_export_invalid_string(self):
        self.assertRaise(
            lambda: images2pdf("/nonexistent/path/image.jpg", "out.pdf"),
            RuntimeError,
        )

    def test_export_invalid_type(self):
        self.assertRaise(
            lambda: images2pdf(42, "out.pdf"),
            TypeError,
        )

    def test_export_verbose(self):
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        datap = os.path.join(os.path.dirname(__file__), "data", "*.jpg")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            dest = f.name
        try:
            res = images2pdf([data, datap], dest, verbose=2)
            self.assertGreater(len(res), 0)
        finally:
            if os.path.exists(dest):
                os.remove(dest)

    def test_export_to_stream(self):
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        stream = io.BytesIO()
        res = images2pdf([data], stream)
        self.assertGreater(stream.tell(), 0)

    def test_export_rotate(self):
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            dest = f.name
        try:
            res = images2pdf([data], dest, rotate=90, verbose=1)
            self.assertExists(dest)
        finally:
            if os.path.exists(dest):
                os.remove(dest)

    def test_export_zoom_with_verbose(self):
        data = os.path.join(os.path.dirname(__file__), "data", "mazures1.jpg")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            dest = f.name
        try:
            res = images2pdf([data], dest, zoom=0.5, verbose=1)
            self.assertExists(dest)
        finally:
            if os.path.exists(dest):
                os.remove(dest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
