====
gdot
====

This directive displays :epkg:`dot` graph in the documentation.

Usage
=====

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.gdot',
    ]

One example:

::

    .. gdot::

        digraph foo {
            "bar" -> "baz" -> "end";
        }

Which gives:

.. gdot::

    digraph foo {
        "bar" -> "baz" -> "end";
    }

The output format is an image (:epkg:`PNG`).
It can be changed to use :epkg:`SVG` but
it requires `viz.js` to be displayed.

::

    .. gdot::
        :format: svg

        digraph foo {
            "bar" -> "baz" -> "svg";
        }

.. gdot::
    :format: svg

    digraph foo {
        "bar" -> "baz" -> "svg";
    }

The graph may also be the output of a script.

::

    .. gdot::
        :format: svg
        :script: AFTER-THIS

        print("before the graph")
        print("AFTER-THIS", """
        digraph foo {
            "bar" -> "baz" -> "script";
        }
        """)

.. gdot::
    :format: svg
    :script: AFTER-THIS

    print("before the graph")
    print("AFTER-THIS", """
    digraph foo {
        "bar" -> "baz" -> "script";
    }
    """)

Finally, the tag `:process:` can be used to run the script in
a separate process.

Directive
=========

.. autoclass:: sphinx_runpython.gdot.sphinx_gdot_extension.GDotDirective
