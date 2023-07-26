from contextlib import redirect_stderr
import io
import os
import sys
import tempfile
from typing import Tuple
from docutils.core import publish_parts
from .runpython import run_cmd

_dummy_extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_issues",
    "sphinx_runpython.blocdefs.sphinx_blocref_extension",
    "sphinx_runpython.blocdefs.sphinx_exref_extension",
    "sphinx_runpython.blocdefs.sphinx_mathdef_extension",
    "sphinx_runpython.collapse",
    "sphinx_runpython.docassert",
    "sphinx_runpython.epkg",
    "sphinx_runpython.runpython",
    "sphinx_runpython.sphinx_rst_builder",
]

_dummy_epkg_dictionary = {
    "autopep8": "https://pypi.org/project/autopep8/",
    "dot": "https://en.wikipedia.org/wiki/DOT_(graph_description_language)",
    "DOT": "https://en.wikipedia.org/wiki/DOT_(graph_description_language)",
    "JIT": "https://en.wikipedia.org/wiki/Just-in-time_compilation",
    "git": "https://git-scm.com/",
    "Graphviz": "https://graphviz.org/",
    "HTML": "https://simple.wikipedia.org/wiki/HTML",
    "nested_parse_with_titles": "http://sphinx-doc.org/extdev/markupapi.html?highlight=nested_parse_with_titles",
    "numpy": (
        "https://www.numpy.org/",
        ("https://docs.scipy.org/doc/numpy/reference/generated/numpy.{0}.html", 1),
        ("https://docs.scipy.org/doc/numpy/reference/generated/numpy.{0}.{1}.html", 2),
    ),
    "pandas": (
        "https://pandas.pydata.org/pandas-docs/stable/",
        ("https://pandas.pydata.org/pandas-docs/stable/generated/pandas.{0}.html", 1),
        (
            "https://pandas.pydata.org/pandas-docs/stable/generated/pandas.{0}.{1}.html",
            2,
        ),
    ),
    "pandoc": "https://johnmacfarlane.net/pandoc/",
    "Pandoc": "https://johnmacfarlane.net/pandoc/",
    "PNG": "https://en.wikipedia.org/wiki/PNG",
    "pypandoc": "https://github.com/JessicaTegner/pypandoc",
    "python": "https://www.python.org/",
    "RST": "https://fr.wikipedia.org/wiki/ReStructuredText",
    "sphinx": "https://www.sphinx-doc.org/en/master/",
    "sphinx-gallery": "https://github.com/sphinx-gallery/sphinx-gallery",
    "SVG": "https://en.wikipedia.org/wiki/SVG",
    "viz.js": "https://visjs.org/",
    "*py": (
        "https://docs.python.org/3/",
        ("https://docs.python.org/3/library/{0}.html", 1),
        ("https://docs.python.org/3/library/{0}.html#{0}.{1}", 2),
        ("https://docs.python.org/3/library/{0}.html#{0}.{1}.{2}", 3),
    ),
    "*pyf": (("https://docs.python.org/3/library/functions.html#{0}", 1),),
}


_dummy_conf = """
import os
import sys
from sphinx_runpython import __version__

source_suffix = ".rst"
master_doc = "index"
project = "rst2html"
pygments_style = "sphinx"
todo_include_todos = True

html_theme = "alabaster"
html_theme_path = ["_static"]
html_theme_options = {}
html_static_path = ["_static"]

"""


def _rst2html_sphinx(
    rst: str, writer_name: str = "html", report_level: int = 0, **kwargs
) -> Tuple[str, str]:
    if "writer" in kwargs:
        raise ValueError("'writer' is not a valid argument, please use 'writer_name'.")
    with tempfile.TemporaryDirectory() as folder:
        index = os.path.join(folder, "index.rst")
        with open(index, "w", encoding="utf-8") as f:
            f.write(rst)
        conf = os.path.join(folder, "conf.py")
        with open(conf, "w", encoding="utf-8") as f:
            f.write(_dummy_conf)
            f.write(f"\nextensions = {_dummy_extensions}\n")
            f.write(f"\nepkg_dictionary = {_dummy_epkg_dictionary}\n")
        fout = os.path.join(folder, "output")

        rep = " -v" * report_level
        cmd = f"{sys.executable} -m sphinx -b {writer_name} {folder} {fout}{rep}"
        out, err = run_cmd(cmd, wait=True)

        html = os.path.join(fout, f"index.{writer_name}")
        if not os.path.exists(html):
            raise RuntimeError(
                f"Unable to find output {html!r}\n--STDOUT--\n{out}\n--STDERR--\n{err}"
            )
        with open(html, "r", encoding="utf-8") as f:
            content = f.read()
        return content, err


def rst2html(
    rst: str,
    writer_name: str = "html",
    report_level: int = 0,
    return_warnings: bool = False,
    use_sphinx: bool = True,
    **kwargs,
) -> Tuple[str, str]:
    """
    Converts a RST string into HTML or RST.

    :param rst: RST string
    :param report_level: filter output, 0 means everything
    :param writer_name: writer name
    :param kwargs: additional values to add to the configuration
    :param return_warnings: return the warnings as well
    :param use_sphinx: run sphinx from the command line and
        returns the results, for that configuration
    :return: output and warnings
    """
    if use_sphinx:
        content, err = _rst2html_sphinx(
            rst, writer_name=writer_name, report_level=report_level, **kwargs
        )
        if return_warnings:
            return content, err
        return content
    docutils_kwargs = {
        "writer_name": writer_name,
        "settings_overrides": {
            "_disable_config": True,
            "report_level": report_level,
        },
    }
    target = io.StringIO()
    with redirect_stderr(target):
        parts = publish_parts(rst, **docutils_kwargs)
        html = parts["html_body"]
        warning = target.getvalue().strip()
        if "System Message: ERROR" in html:
            raise RuntimeError(
                f"rst2html failed, warnings:\n{warning}\n-----\nOUTPUT\n{html}"
            )
        if return_warnings:
            return html, warning
        return html
