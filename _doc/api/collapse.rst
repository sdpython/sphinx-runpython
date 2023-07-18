========
collapse
========

This directive hides or unhides a part of the documentation, usually
snippets of code. The user can click on a button to fold or unfold
a section.

Usage
=====

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.collapse',
    ]

.. sidebar:: collapse

    ::

        .. collapse::

            Show or hide a part of the documentation.

.. collapse::

    Show or hide a part of the documentation.

Directive
=========

.. autoclass:: sphinx_runpython.collapse.sphinx_collapse_extension.CollapseDirective
