========
blocdefs
========

They pretty much follows the same design. They highlight a paragraph
and this paragraph can be recalled anywhere on another page. Some options
differs depending on the content.

List of bloc extensions
=======================

* :class:`BlocRef <sphinx_runpython.blocdefs.sphinx_blocref_extension.BlocRef>`:
  to add a definition (or any kind of definition)
* :class:`ExRef <sphinx_runpython.blocdefs.sphinx_exref_extension.ExRef>`:
  to add an example
* :class:`mathdef <sphinx_runpython.blocdefs.sphinx_mathdef_extension.MathDef>`:
  to add a mathematical definition (or any kind of definition)

exref
=====

Location: :class:`ExRef <sphinx_runpython.blocdefs.sphinx_exref_extension.ExRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_exref_extension']

    exref_include_exrefs = True

.. sidebar:: exref

    ::

        .. exref::
            :title: How to add an example?
            :tag: example
            :label: l-this-example

            This example, a piece of code...

.. exref::
    :title: How to add an example?
    :tag: example
    :label: this-faq-example

    This example, a piece of code...

A reference can be added to this example :ref:`l-this-example`.
And all examples can be replicated with commad `exreflist`
for a specific tag.

.. sidebar:: exreflist

    ::

        .. exreflist::
            :tag: example
            :contents:

.. exreflist::
    :tag: example
    :contents:

blocref
=======

Location: :class:`BlocRef <sphinx_runpython.blocdefs.sphinx_blocref_extension.BlocRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_blocref_extension']

    blocref_include_blocrefs = True

.. sidebar:: blocref

    ::

        .. blocref::
            :title: How to add a bloc?
            :tag: bloc
            :label: l-this-bloc

            A bloc...

.. blocref::
    :title: How to add a bloc?
    :tag: bloc
    :label: l-this-bloc

    A bloc...

A reference can be added to this bloc :ref:`l-this-bloc`.
And all examples can be replicated with commad `exblocreflist`
for a specific tag.

.. sidebar:: exblocreflist

    ::

        .. exblocreflist::
            :tag: bloc
            :contents:

.. exblocreflist::
    :tag: bloc
    :contents:

mathref
=======

Location: :class:`MathRef <sphinx_runpython.blocdefs.sphinx_mathdef_extension.MathRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_mathdef_extension']

    mathdef_include_mathdefs = True

.. sidebar:: mathdef

    ::

        .. mathdef::
            :title: How to add a definition?
            :tag: definition
            :label: l-this-def

            A definition...

.. mathdef::
    :title: How to add a definition?
    :tag: definition
    :label: l-this-def

    A definition...

A reference can be added to this definition :ref:`l-this-def`.
And all examples can be replicated with commad `exmathdeflist`
for a specific tag.

.. sidebar:: exmathdeflist

    ::

        .. exmathdeflist::
            :tag: definition
            :contents:

.. exmathdeflist::
    :tag: definition
    :contents:

