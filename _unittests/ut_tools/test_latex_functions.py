import unittest
from sphinx_runpython.ext_test_case import ExtTestCase, hide_stdout
from sphinx_runpython.tools.latex_functions import build_regex, replace_latex_command


class TestLatexFunction(ExtTestCase):

    def test_build_regex(self):
        regs = build_regex()
        self.assertEqual(regs["supegal"], "\\geqslant")

    @hide_stdout()
    def test_replace_pattern(self):
        self.assertEqual(replace_latex_command("\\R"), "\\mathbb{R}")
        self.assertEqual(replace_latex_command("A\\R B"), "A\\mathbb{R} B")
        self.assertEqual(replace_latex_command("\\pa{5+3i}"), "\\left(5+3i\\right)")
        self.assertEqual(replace_latex_command("A\\pa{5+3i}B"), "A\\left(5+3i\\right)B")
        self.assertEqual(replace_latex_command("\\cro{5+3i}"), "\\left[5+3i\\right]")
        self.assertEqual(
            replace_latex_command("\\acc{5+3i}"), "\\left\\{5+3i\\right\\}"
        )
        self.assertEqual(
            replace_latex_command("\\vecteur{a}{b}"), "\\left(a,\\dots,b\\right)"
        )
        self.assertEqual(
            replace_latex_command("\\pa{5\\pa{3i+3}}"),
            "\\left(5\\left(3i+3\\right)\\right)",
        )
        self.assertEqual(
            replace_latex_command("\\pa{5+3i}\\pa{3i+3}"),
            "\\left(5+3i\\right)\\left(3i+3\\right)",
        )
        self.assertEqual(
            replace_latex_command(
                "\\indicatrice{ N \\supegal X } +  \\cro{ X (s-p) + N (q-s)} "
                "\\indicatrice{ N < X }",
                verbose=1,
            ),
            " {1\\!\\!1}_{\\left\\{ N \\geqslant X \\right\\}}  +  "
            "\\left[ X (s-p) + N (q-s)\\right]"
            "  {1\\!\\!1}_{\\left\\{ N < X \\right\\}} ",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
