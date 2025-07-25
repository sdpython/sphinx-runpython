.. _l-sphinx-epkg:

====
epkg
====

This role can be used to store urls in the configuration file and
only show the anchor in the documentation.

Usage
=====

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.epkg',
    ]

    epkg_dictionary = {
        'pandoc': 'https://pandoc.org/',                                            # 1
        'pandas': (
            'https://pandas.pydata.org/docs/',                                      # 2
            ('https://pandas.pydata.org/docs/reference/api/pandas.{0}.html', 1)),   # 3
        }

The variable ``epkg_dictionary`` stores the list of url to display. It can be a simple
string or a list of possibililies with multiple parameters. The three options above can
used like this. The last one allows one parameter separated by ``:``.

.. sidebar:: epkg

    ::

        * Option 1: :epkg:`pandoc`
        * Option 2: :epkg:`pandas`,
        * Option 3: :epkg:`pandas:DataFrame`

* Option 1: :epkg:`pandoc`
* Option 2: :epkg:`pandas`,
* Option 3: :epkg:`pandas:DataFrame`

The last link is broken before the current file is not python
file but a *rst*. The file extension must be specified.
For some websites, url and functions do not follow the same rule.
A function must be used in this case to handle the mapping.

::

    def weird_mapping(input):
        # The function receives whatever is between `...`.
        ...
        return anchor, url

This function must be placed at the end or be the only available option.

::

    epkg_dictionary = { 'weird_site': weird_mapping }

However, because it is impossible to use a function as a value
in the configuration because :epkg:`*py:pickle` does not handle
this scenario (see `PicklingError on environment when config option
value is a callable <https://github.com/sphinx-doc/sphinx/issues/1424>`_),
``my_custom_links`` needs to be replaced by:
``("module_where_it_is_defined.my_custom_links", None)``.
The role *epkg* will import it based on its name.

Directive
=========

.. autofunction:: sphinx_runpython.epkg.sphinx_epkg_extension.epkg_role
