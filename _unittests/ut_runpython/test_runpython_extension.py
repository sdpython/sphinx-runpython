import sys
import unittest
from docutils.parsers.rst import directives
from sphinx_runpython.helpers import rst2html
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.runpython.sphinx_runpython_extension import (
    RunPythonDirective,
    runpython_node,
    visit_runpython_node,
    depart_runpython_node,
)

tives = [
    (
        "runpython",
        RunPythonDirective,
        runpython_node,
        visit_runpython_node,
        depart_runpython_node,
    )
]


class TestRunPythonExtension(ExtTestCase):
    def test_post_parse(self):
        directives.register_directive("runpython", RunPythonDirective)

    def test_runpython(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :rst:
                        :showcode:

                        print(u"this code shoud appear" + u"___")
                        import sys
                        print(u"setsysvar: " + str(
                            sys.__dict__.get(
                                'enable_disabled_documented_pieces_of_code', None)))
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t1 = "this code shoud appear___"
        if t1 not in html:
            raise AssertionError(html)
        t2 = "setsysvar: True"
        if t2 not in html:
            raise AssertionError(html)
        t2 = "<p>&lt;&lt;&lt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        t2 = "<p>&gt;&gt;&gt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

    def test_runpython_numpy(self):
        """
        this test also test the extension runpython
        """
        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :rst:
                        :showcode:
                        :numpy_precision: 2

                        import numpy
                        print(numpy.array([1.123456789, 1.987654321]))
                    """.replace(
            "                    ", ""
        )

        html = rst2html(content, writer="rst", keep_warnings=True, directives=tives)
        if "[1.12 1.99]" not in html:
            raise AssertionError(html)

    def test_runpython_numpy_linenos(self):
        """
        this test also test the extension runpython
        """
        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :rst:
                        :showcode:
                        :numpy_precision: 2
                        :linenos:

                        import numpy
                        print(numpy.array([1.123456789, 1.987654321]))
                    """.replace(
            "                    ", ""
        )

        html = rst2html(content, writer="rst", keep_warnings=True, directives=tives)
        if "[1.12 1.99]" not in html:
            raise AssertionError(html)
        self.assertIn(":linenos:", html)

        html = rst2html(content, writer="html", keep_warnings=True, directives=tives)
        self.assertIn('class="linenos">', html)

    def test_runpython_catch_warning(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :rst:
                        :showcode:
                        :warningout: DeprecationWarning

                        import warnings
                        warnings.warn("deprecated", DeprecationWarning)
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t1 = ": DeprecationWarning: deprecated"
        if t1 in html:
            raise AssertionError(html)

    def test_runpython_notcatch_warning(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :rst:
                        :showcode:

                        import warnings
                        warnings.warn("deprecated", DeprecationWarning)
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t1 = "DeprecationWarning"
        if t1 not in html:
            raise AssertionError(html)

    def test_runpython_raw(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:

                        print(u"this code shoud appear" + u"___")
                        import sys
                        print(u"setsysvar: " + str(sys.__dict__.get(
                            'enable_disabled_documented_pieces_of_code', None)))
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t1 = "this code shoud appear___"
        for t in t1.split():
            if t not in html:
                raise AssertionError(html)
        t2 = "setsysvar: True"
        for t in t2.split():
            if t.strip(":") not in html:
                raise AssertionError(html)
        t2 = "<p>&gt;&gt;&gt;</p>"
        if t2 in html:
            raise AssertionError(html)
        t2 = "<p>Out</p>"
        if t2 in html:
            raise AssertionError(html)
        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

    def test_runpython_process(self):
        """
        this test also test the extension runpython
        """
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :setsysvar:
                        :process:
                        :showcode:

                        import sphinx_runpython
                        print(u"this code shoud appear" + u"___")
                        import sys
                        print(u"setsysvar: " + str(sys.__dict__.get(
                            'enable_disabled_documented_pieces_of_code', None)))
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t1 = "this code shoud appear___"
        for t in t1.split():
            if t not in html:
                raise AssertionError(html)
        t2 = "setsysvar: True"
        for t in t2:
            if t.strip(";") not in html:
                raise AssertionError(html)
        t2 = "<p>&lt;&lt;&lt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        t2 = "<p>&gt;&gt;&gt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

    def test_runpython_exception(self):
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :showcode:
                        :exception:

                        print(u"this code shoud" + u" appear")
                        z = 1/0
                        print(u"this one should" + u" not")
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t2 = "<p>&lt;&lt;&lt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        t2 = "<p>&gt;&gt;&gt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        if "ZeroDivisionError" not in html:
            raise AssertionError(html)

    def test_runpython_exception_assert(self):
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :showcode:
                        :assert: z == 1.1

                        print(u"this code shoud" + u" appear")
                        z = 0.5 + 0.6
                        print(u"this one should" + u" not")
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t2 = "<p>&lt;&lt;&lt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        t2 = "<p>&gt;&gt;&gt;</p>"
        if t2 not in html:
            raise AssertionError(html)

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :showcode:
                        :assert: z == 1.2

                        z = 0.5 + 0.6
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        try:
            html = rst2html(
                content,
                writer="custom",
                keep_warnings=True,
                directives=tives,
            )
        except Exception as e:
            if "Condition 'z == 1.2' failed" not in str(e):
                raise e

    def test_runpython_process_exception(self):
        from docutils import nodes

        class runpythonthis_node(nodes.Structural, nodes.Element):
            pass

        class RunPythonThisDirective(RunPythonDirective):
            runpython_class = runpythonthis_node

        def visit_rp_node(self, node):
            "local function"
            self.body.append("<p><b>visit_rp_node</b></p>")

        def depart_rp_node(self, node):
            self.body.append("<p><b>depart_rp_node</b></p>")

        if "enable_disabled_documented_pieces_of_code" in sys.__dict__:
            raise AssertionError("this case shoud not be")

        content = """
                    test a directive
                    ================

                    .. runpythonthis::
                        :showcode:
                        :exception:
                        :process:

                        print(u"this code shoud" + u" appear")
                        z = 1/0
                        print(u"this one should" + u" not")
                    """.replace(
            "                    ", ""
        )
        content = content.replace('u"', '"')

        tives = [
            (
                "runpythonthis",
                RunPythonThisDirective,
                runpythonthis_node,
                visit_rp_node,
                depart_rp_node,
            )
        ]

        html = rst2html(content, writer="custom", keep_warnings=True, directives=tives)

        t2 = "<p>&lt;&lt;&lt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        t2 = "<p>&gt;&gt;&gt;</p>"
        if t2 not in html:
            raise AssertionError(html)
        if "ZeroDivisionError" not in html:
            raise AssertionError(html)


if __name__ == "__main__":
    unittest.main()
