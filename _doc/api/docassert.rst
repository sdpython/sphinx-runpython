=========
docassert
=========

This extension checks that functions or classes have not
undocumented parameters.

Usage
=====

Location: :class:`docassert setup <sphinx_runpython.docassert.sphinx_docassert_extension.OverrideDocFieldTransformer>`.

This extension does nothing but generating warnings if a function or a class
documents a misspelled parameter (not in the signature) or if one
parameter is missing from the documentation.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_docassert_extension']

Sphinx outputs some warnings:

::

    WARNING: [docassert] '_init' has undocumented parameters 'translator_class' (in 'pyquickhelper\_doc\sphinxdoc\source\pyquickhelper\helpgen\sphinxm_convert_doc_sphinx_helper.py').

Classes
=======

.. autoclass:: sphinx_runpython.docassert.sphinx_docassert_extension.OverrideDocFieldTransformer