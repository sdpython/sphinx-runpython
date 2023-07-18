.. _l-blodefs:

=======================
blocref, exref, mathdef
=======================

They pretty much follows the same design. They highlight a paragraph
and this paragraph can be recalled anywhere on another page. Some options
differs depending on the content.

exref
=====

Location: :class:`exref <sphinx_runpython.blocdefs.sphinx_exref_extension.ExRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_exref_extension']

    exref_include_exrefs = True

An example:

::

    .. exref::
        :title: How to add an example?
        :tag: example
        :label: l-this-example

        This example, a piece of code...

Which gives:

.. exref::
    :title: How to add an example?
    :tag: example
    :label: this-faq-example

    This example, a piece of code...

A reference can be added to this example :ref:`l-this-example`.

blocref
=======

Location: :class:`blocref <sphinx_runpython.blocdefs.sphinx_blocref_extension.BlocRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_blocref_extension']

    blocref_include_blocrefs = True

An example:

::

    .. blocref::
        :title: How to add a bloc?
        :tag: bloc
        :label: l-this-bloc

        A bloc...

Which gives:

.. blocref::
    :title: How to add a bloc?
    :tag: bloc
    :label: l-this-bloc

    A bloc...

A reference can be added to this bloc :ref:`l-this-bloc`.

mathdef
=======

Location: :class:`mathdef <sphinx_runpython.blocdefs.sphinx_mathdef_extension.MathDef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_mathdef_extension']

    mathdef_include_mathdefs = True

An example:

::

    .. mathdef::
        :title: How to add a definition?
        :tag: definition
        :label: l-this-def

        A definition...

Which gives:

.. mathdef::
    :title: How to add a definition?
    :tag: definition
    :label: l-this-def

    A definition...

A reference can be added to this definition :ref:`l-this-def`.
