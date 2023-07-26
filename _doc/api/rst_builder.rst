==================
sphinx_rst_builder
==================

This directive outputs the documentation in :epkg:`RST` format
with all the sphinx directives converted into pure RST format.

Usage
=====

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.sphinx_rst_builder',
    ]

Classes
=======

RstBuilder
++++++++++

.. autoclass:: sphinx_runpython.gdot.sphinx_gdot_extension.RstBuilder
    :members:

RstTranslator
+++++++++++++

.. autoclass:: sphinx_runpython.gdot.sphinx_gdot_extension.RstTranslator
    :members:

RstWriter
+++++++++

.. autoclass:: sphinx_runpython.gdot.sphinx_gdot_extension.RstWriter
    :members:
