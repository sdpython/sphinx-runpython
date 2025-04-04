.. _l-blocdefs:

=======================
blocref, exref, mathdef
=======================

They pretty much follows the same design. They highlight a paragraph
and this paragraph can be recalled anywhere on another page. Some options
differs depending on the content.

exref
=====

Location: :class:`ExRef <sphinx_runpython.blocdefs.sphinx_exref_extension.ExRef>`.

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
    :label: l-this-example

    This example, a piece of code...

A reference can be added to this example :ref:`Example 1 <l-this-example>`.
The title needs to be recalled.

faqref
======

Location: :class:`FaqRef <sphinx_runpython.blocdefs.sphinx_faqref_extension.FaqRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_faqref_extension']

    faqref_include_faqrefs = True

An example:

::

    .. faqref::
        :title: How to add an example?
        :tag: faq1
        :label: l-this-faq

        This example, a piece of code...

Which gives:

.. faqref::
    :title: How to add an example?
    :tag: faq1
    :label: l-this-faq

    This example, a piece of code...

A reference can be added to this example :ref:`Faq 1 <l-this-faq>`.
The title needs to be recalled.

blocref
=======

Location: :class:`BlocRef <sphinx_runpython.blocdefs.sphinx_blocref_extension.BlocRef>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.blocdefs.sphinx_blocref_extension']

    blocref_include_blocrefs = True

An example:

::

    .. blocref::
        :title: How to add a block?
        :tag: block
        :label: l-this-block

        A block...

Which gives:

.. blocref::
    :title: How to add a block?
    :tag: block
    :label: l-this-block

    A block...

A reference can be added to this block :ref:`Block A <l-this-block>`.
The title needs to be recalled.

mathdef
=======

Location: :class:`MathDef <sphinx_runpython.blocdefs.sphinx_mathdef_extension.MathDef>`.

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

A reference can be added to this definition :ref:`Def 1 <l-this-def>`.
The title needs to be recalled.

Directives
==========

.. autoclass:: sphinx_runpython.blocdefs.sphinx_blocref_extension.BlocRef
    :members:

.. autoclass:: sphinx_runpython.blocdefs.sphinx_exref_extension.ExRef
    :members:

.. autoclass:: sphinx_runpython.blocdefs.sphinx_faqref_extension.FaqRef
    :members:

.. autoclass:: sphinx_runpython.blocdefs.sphinx_mathdef_extension.MathDef
    :members:

Nodes
=====

.. autoclass:: sphinx_runpython.blocdefs.sphinx_blocref_extension.blocref_node

.. autoclass:: sphinx_runpython.blocdefs.sphinx_exref_extension.exref_node

.. autoclass:: sphinx_runpython.blocdefs.sphinx_faqref_extension.faqref_node

.. autoclass:: sphinx_runpython.blocdefs.sphinx_mathdef_extension.mathdef_node
