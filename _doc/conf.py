# coding: utf-8
import os
import sys
from sphinx_runpython import __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_gallery.gen_gallery",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_runpython.blocdefs.sphinx_blocref_extension",
    "sphinx_runpython.blocdefs.sphinx_exref_extension",
    "sphinx_runpython.blocdefs.sphinx_mathdef_extension",
    "sphinx_runpython.collapse",
    "sphinx_runpython.epkg",
    "sphinx_runpython.runpython",
]

templates_path = ["_templates"]
html_logo = "_static/logo.png"
source_suffix = ".rst"
master_doc = "index"
project = "sphinx-runpython"
copyright = "2023, Xavier Dupré"
author = "Xavier Dupré"
version = __version__
release = __version__
language = "en"
exclude_patterns = []
pygments_style = "sphinx"
todo_include_todos = True

html_theme = "furo"
html_theme_path = ["_static"]
html_theme_options = {}
html_static_path = ["_static"]


intersphinx_mapping = {
    "matplotlib": ("https://matplotlib.org/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "python": (f"https://docs.python.org/{sys.version_info.major}", None),
}

sphinx_gallery_conf = {
    # path to your examples scripts
    "examples_dirs": os.path.join(os.path.dirname(__file__), "examples"),
    # path where to save gallery generated examples
    "gallery_dirs": "auto_examples",
}

epkg_dictionary = {
    "DOT": "https://graphviz.org/doc/info/lang.html",
    "JIT": "https://en.wikipedia.org/wiki/Just-in-time_compilation",
    "git": "https://git-scm.com/",
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
    "python": "https://www.python.org/",
    "RST": "https://fr.wikipedia.org/wiki/ReStructuredText",
    "sphinx-gallery": "https://github.com/sphinx-gallery/sphinx-gallery",
    "*py": (
        "https://docs.python.org/3/",
        ("https://docs.python.org/3/library/{0}.html", 1),
        ("https://docs.python.org/3/library/{0}.html#{0}.{1}", 2),
        ("https://docs.python.org/3/library/{0}.html#{0}.{1}.{2}", 3),
    ),
    "*pyf": (("https://docs.python.org/3/library/functions.html#{0}", 1),),
}
