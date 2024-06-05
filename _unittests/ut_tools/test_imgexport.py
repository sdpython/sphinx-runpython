import os
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
