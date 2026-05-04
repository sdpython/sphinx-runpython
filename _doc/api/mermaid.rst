=======
mermaid
=======

This directive displays `Mermaid <https://mermaid.js.org/>`_ diagrams in the documentation.
Diagrams are rendered client-side in *HTML* output via the Mermaid JavaScript library
and as verbatim text in *LaTeX* / *RST* output.

Usage
=====

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.mermaid',
    ]

One example:

::

    .. mermaid::

        graph LR
            A --> B --> C

Which gives:

.. mermaid::

    graph LR
        A --> B --> C

The diagram source can also be produced by a Python script.
Option *script* must be specified:

::

    .. mermaid::
        :script:

        print("""
        graph LR
            A --> B
        """)

.. mermaid::
    :script:

    print("""
    graph LR
        A --> B
    """)

When *script* is a non-empty string it is used as a split token: only
the output **after** the first occurrence of that string is interpreted
as Mermaid source:

::

    .. mermaid::
        :script: AFTER-THIS

        print("preamble")
        print("AFTER-THIS")
        print("graph TD")
        print("    P --> Q")

Finally, the option ``:process:`` can be used to run the script in
a separate process.

Directive
=========

.. autoclass:: sphinx_runpython.mermaid.sphinx_mermaid_extension.MermaidDirective
