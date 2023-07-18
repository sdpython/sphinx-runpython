=========
runpython
=========

This directive executes snippets of code inserted and add
the output to the documentation, as plain text or even RST format.

Usage
=====

Location: :class:`RunPythonDirective <sphinx_runpython.runpython.sphinx_runpython_extension.RunPythonDirective>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.runpython',
    ]

Documentation means many examples which needs to be updated when a change
happen unless the documentation runs the example itself and update its output.
That's what this directive does. It adds as raw text whatever comes out
throught the standard output.

One example:

::

    .. runpython::
        :showcode:

        import os
        for i, name in enumerate(os.listdir(".")):
            print(i, name)

Which gives:

.. runpython::
    :showcode:

    import os
    for i, name in enumerate(os.listdir(".")):
        print(i, name)

The output can also be compiled as RST format and the code can be hidden.
It is useful if the documentation is a copy/paste of some external process
or function. This function can be directly called from the documentation.
The output must be converted into RST format. It is then added to the
documentation. It is quite useful to display the version of some installed
modules.

.. sidebar:: runpython and rst

    ::

        .. runpython::
            :rst:

            import pandas, numpy, sphinx

            for i, mod in [sphinx, pandas, numpy]:
                print("* version of *{0}*: *{1}*".format(
                    getattr(mod, "__name__"), getattr(mod, "__version__"
                ))

.. runpython::
    :rst:

    import os
    for i, name in enumerate(os.listdir(".")):
        print("* file **{0}**: *{1}*".format(i, name))

If the code throws an exception (except a syntax error),
it can be caught by adding the option ``:exception:``.
The directive displays the traceback.

.. runpython::
    :showcode:
    :exception:

    import os
    for i, name in enumerate(os.listdir("not existing")):
        pass

The directive can also be used to display images
with a tweak however. It consists in writing *rst*
code. The variable ``__WD__`` indicates the local
directory.

.. runpython::
    :showcode:

    print('__WD__=%r' % __WD__)

Applied to images...

.. sidebar:: runpython and image

    ::

        .. runpython::
            :rst:

            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 1, figsize=(4, 4))
            ax.plot([0, 1], [0, 1], '--')
            fig.savefig(os.path.join(__WD__, "oo.png"))

            text = ".. image:: oo.png"
            print(text)

The image needs to be save in the same folder than
the *rst* file.

.. runpython::
    :rst:

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))
    ax.plot([0, 1], [0, 1], '--')
    fig.savefig(os.path.join(__WD__, "oo.png"))

    text = ".. image:: oo.png\n    :width: 201px"
    print(text)

Option ``:toggle:`` can hide the code or the output or both
but let the user unhide it by clicking on a button.

.. sidebar:: runpython and image

    ::

        .. runpython::
            :showcode:
            :toggle: out

            for i in range(0, 10):
                print("i=", i)

.. runpython::
    :showcode:
    :toggle: out

    for i in range(0, 10):
        print("i=", i)

The last option of *runpython* allows the user to keep
some context from one execution to the next one.

.. sidebar:: runpython and context

    ::

        .. runpython::
            :showcode:
            :store:

            a_to_keep = 5
            print("a_to_keep", "=", a_to_keep)

        .. runpython::
            :showcode:
            :restore:

            a_to_keep += 5
            print("a_to_keep", "=", a_to_keep)

.. runpython::
    :showcode:
    :store:

    a_to_keep = 5
    print("a_to_keep", "=", a_to_keep)

.. runpython::
    :showcode:
    :restore:

    a_to_keep += 5
    print("a_to_keep", "=", a_to_keep)

.. index:: sphinx-autorun

`sphinx-autorun <https://pypi.org/project/sphinx-autorun/>`_ offers a similar
service except it cannot produce compile :epkg:`RST` content,
hide the source and a couple of other options.

Interesting functions
=====================

.. autofunction:: sphinx_runpython.runpython.run_cmd

.. autofunction:: sphinx_runpython.runpython.sphinx_runpython_extension.remove_extra_spaces_and_pep8

Directive
=========

.. autoclass:: sphinx_runpython.runpython.sphinx_runpython_extension.RunPythonDirective
