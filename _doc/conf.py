import os
import sys
from sphinx_runpython import __version__
from sphinx_runpython.github_link import make_linkcode_resolve
from sphinx_runpython.conf_helper import has_dvipng, has_dvisvgm

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_gallery.gen_gallery",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_issues",
    "sphinx_runpython.blocdefs.sphinx_blocref_extension",
    "sphinx_runpython.blocdefs.sphinx_exref_extension",
    "sphinx_runpython.blocdefs.sphinx_faqref_extension",
    "sphinx_runpython.blocdefs.sphinx_mathdef_extension",
    "sphinx_runpython.collapse",
    "sphinx_runpython.docassert",
    "sphinx_runpython.gdot",
    "sphinx_runpython.epkg",
    "sphinx_runpython.quote",
    "sphinx_runpython.runpython",
    "sphinx_runpython.sphinx_rst_builder",
]

if has_dvisvgm():
    extensions.append("sphinx.ext.imgmath")
    imgmath_image_format = "svg"
elif has_dvipng():
    extensions.append("sphinx.ext.pngmath")
    imgmath_image_format = "png"
else:
    extensions.append("sphinx.ext.mathjax")

templates_path = ["_templates"]
html_logo = "_static/logo.png"
source_suffix = ".rst"
master_doc = "index"
project = "sphinx-runpython"
copyright = "2023-2024, Xavier Dupré"
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

html_sourcelink_suffix = ""

# The following is used by sphinx.ext.linkcode to provide links to github
linkcode_resolve = make_linkcode_resolve(
    "sphinx-runpython",
    (
        "https://github.com/sdpython/sphinx-runpython/"
        "blob/{revision}/{package}/"
        "{path}#L{lineno}"
    ),
)

latex_elements = {
    "papersize": "a4",
    "pointsize": "10pt",
    "title": project,
}

# Check intersphinx reference targets exist
nitpicky = True
# See also scikit-learn/scikit-learn#26761
nitpick_ignore = [
    ("py:class", "False"),
    ("py:class", "True"),
    ("py:class", "SphinxPostTransform"),
    ("py:meth", "Builder.get_relative_uri"),
]

nitpick_ignore_regex = [
    ("py:class", ".*numpy[.].*"),
    ("py:func", ".*[.]PyCapsule[.].*"),
    ("py:func", ".*numpy[.].*"),
    ("py:func", ".*scipy[.].*"),
    ("py:meth", "Builder[.].*"),
]

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
    "automodule": "https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-automodule",
    "black": "https://black.readthedocs.io/en/stable/index.html",
    "dot": "https://en.wikipedia.org/wiki/DOT_(graph_description_language)",
    "DOT": "https://en.wikipedia.org/wiki/DOT_(graph_description_language)",
    "JIT": "https://en.wikipedia.org/wiki/Just-in-time_compilation",
    "git": "https://git-scm.com/",
    "Graphviz": "https://graphviz.org/",
    "HTML": "https://simple.wikipedia.org/wiki/HTML",
    "nested_parse_with_titles": "https://www.sphinx-doc.org/en/master/extdev/markupapi.html#parsing-directive-content-as-rest",
    "numpy": (
        "https://www.numpy.org/",
        ("https://docs.scipy.org/doc/numpy/reference/generated/numpy.{0}.html", 1),
        ("https://docs.scipy.org/doc/numpy/reference/generated/numpy.{0}.{1}.html", 2),
    ),
    "pandas": (
        "https://pandas.pydata.org/docs/reference/index.html",
        ("https://pandas.pydata.org/docs/reference/api/pandas.{0}.html", 1),
        ("https://pandas.pydata.org/docs/reference/api/pandas.{0}.{1}.html", 2),
    ),
    "pandoc": "https://pandoc.org/",
    "Pandoc": "https://pandoc.org/",
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
