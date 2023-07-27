
.. image:: https://github.com/sdpython/sphinx-runpython/raw/main/_doc/_static/logo.png
    :width: 120

sphinx-runpython: run python code in sphinx
===========================================

.. image:: https://dev.azure.com/xavierdupre3/sphinx-runpython/_apis/build/status/sdpython.sphinx-runpython
    :target: https://dev.azure.com/xavierdupre3/sphinx-runpython/

.. image:: https://badge.fury.io/py/sphinx-runpython.svg
    :target: http://badge.fury.io/py/sphinx-runpython

.. image:: http://img.shields.io/github/issues/sdpython/sphinx-runpython.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/sphinx-runpython/issues

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: https://opensource.org/license/MIT/

.. image:: https://img.shields.io/github/repo-size/sdpython/sphinx-runpython
    :target: https://github.com/sdpython/sphinx-runpython/
    :alt: size

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://codecov.io/github/sdpython/sphinx-runpython/branch/main/graph/badge.svg?token=CTUV6EDBB6 
    :target: https://codecov.io/github/sdpython/sphinx-runpython

**sphinx-runpython** implements sphinx extensions including one
to execute code and add the output to the documentation.
The library is released on
`pypi/sphinx-runpython <https://pypi.org/project/sphinx-runpython/>`_
and its documentation is published at
`sphinx-runpython
<https://sdpython.github.io/doc/sphinx-runpython/dev/>`_.

epkg
++++

It implements a list of recurring urls in documentation.

**conf.py**

::

    epkg_dictionary = {'title': 'url' }

**rst**

::

    :epkg:`title`  -> `title <url>`_


runpython
+++++++++

Executes code in the documentation and adds it to documentation.

::

    .. runpython::
        :showcode:

        print("python code")

::

    <<<

    print("python code")

    >>>

    python code

List of directives
++++++++++++++++++

* `blocref <https://sdpython.github.io/doc/sphinx-runpython/dev/api/blocdefs.html>`_
* `collapse <https://sdpython.github.io/doc/sphinx-runpython/dev/api/collapse.html>`_
* `docassert <https://sdpython.github.io/doc/sphinx-runpython/dev/api/docassert.html>`_
* `epkg <https://sdpython.github.io/doc/sphinx-runpython/dev/api/epkg.html>`_
* `exref <https://sdpython.github.io/doc/sphinx-runpython/dev/api/blocdefs.html>`_
* `gdot <https://sdpython.github.io/doc/sphinx-runpython/dev/api/gdot.html>`_
* `mathdef <https://sdpython.github.io/doc/sphinx-runpython/dev/api/blocdefs.html>`_
* `runpython <https://sdpython.github.io/doc/sphinx-runpython/dev/api/runpython.html>`_
* `sphinx_rst_builder <https://sdpython.github.io/doc/sphinx-runpython/dev/api/rst_builder.html>`_
