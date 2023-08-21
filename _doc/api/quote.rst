=====
quote
=====

A bloc to insert a quote from a book, a film...

Usage
=====

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.quote',
    ]

One example:

::

    .. quote::
        :author: Esther Duflo
        :book: Expérience, science et lutte contre la pauvreté
        :year: 2013
        :index: economy
        :pages: 26

        [Roosevelt] It is common sense to take a method and try it:
        if it fails, admit frankly and try another. But above all,
        try something.

Which gives:

.. quote::
    :author: Esther Duflo
    :book: Expérience, science et lutte contre la pauvreté
    :year: 2013
    :index: pauvreté
    :pages: 26

    [Roosevelt] It is common sense to take a method and try it:
    if it fails, admit frankly and try another. But above all,
    try something.

Directive
=========

.. autoclass:: sphinx_runpython.quote.sphinx_quote_extension.QuoteNode
