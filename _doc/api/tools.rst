=====
tools
=====

Checks the readme syntax
========================

The command line checks the readme syntax in virtual environments.

::

    python -m sphinx_runpython readme -p <path_to_readme.rst> -v

It is based on function:

.. autofunction:: sphinx_runpython.readme.check_readme_syntax

However, it is better to run command line ``twine check dist/*``
assuming the whl was built by a command such as ``python setup.py sdist``.

Convert notebooks into examples
===============================

The command line converts every notebook in a folder
into examples which can be used into a sphinx gallery.

::

    python -m sphinx_runpython --help

Tools related to latex
======================

.. autofunction:: sphinx_runpython.tools.latex_functions.build_regex

.. autofunction:: sphinx_runpython.tools.latex_functions.replace_latex_command
