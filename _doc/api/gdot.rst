====
gdot
====

This directive displays :epkg:`dot` graph in the documentation.

Usage
=====

Location: :func:`gdot <sphinx_runpython.gdot.sphinx_gdot_extension.GDotDirective>`.

In *conf.py*:

::

    extensions = [ ...
        'sphinx_runpython.gdot',
    ]

One example:

::

    .. gdot::

        digraph tree {
            A [label="X1 &lt; 5",shape=record];
            B [label="X2 &lt; 3",shape=record];
            C [label="X3 &lt; 2",shape=record];
            A -> B;
            A -> C;
            D [label="<c0> 0|<c1> 1",shape=record];
            E [label="<c0> 0|<c1> 1",shape=record];
            B -> D:c0;
            B -> D:c1;
            C -> E:c0;
            C -> E:c1;
        }

Which gives:

.. gdot::

    digraph tree {
        A [label="X1 &lt; 5",shape=record];
        B [label="X2 &lt; 3",shape=record];
        C [label="X3 &lt; 2",shape=record];
        A -> B;
        A -> C;
        D [label="<c0> 0|<c1> 1",shape=record];
        E [label="<c0> 0|<c1> 1",shape=record];
        B -> D:c0;
        B -> D:c1;
        C -> E:c0;
        C -> E:c1;
    }

The output format is an image (:epkg:`PNG`).
It can be changed to use :epkg:`SVG` but
it requires `viz.js` to be displayed.

::

    .. gdot::
        :format: svg

        digraph tree {
            A [label="X1 &lt; 5",shape=record];
            B [label="X2 &lt; 3",shape=record];
            C [label="X3 &lt; 2",shape=record];
            A -> B;
            A -> C;
            D [label="<c0> 0|<c1> 1",shape=record];
            E [label="<c0> 0|<c1> 1",shape=record];
            B -> D:c0;
            B -> D:c1;
            C -> E:c0;
            C -> E:c1;
        }

.. gdot::
    :format: svg

    digraph tree {
        A [label="X1 &lt; 5",shape=record];
        B [label="X2 &lt; 3",shape=record];
        C [label="X3 &lt; 2",shape=record];
        A -> B;
        A -> C;
        D [label="<c0> 0|<c1> 1",shape=record];
        E [label="<c0> 0|<c1> 1",shape=record];
        B -> D:c0;
        B -> D:c1;
        C -> E:c0;
        C -> E:c1;
    }

The graph may also be the output of a script.

::

    .. gdot::
        :format: svg
        :script: AFTER-THIS

        print("before the graph")
        print("AFTER-THIS", """
        digraph tree {
            A [label="X1 &lt; 5",shape=record];
            B [label="X2 &lt; 3",shape=record];
            C [label="X3 &lt; 2",shape=record];
            A -> B;
            A -> C;
            D [label="<c0> 0|<c1> 1",shape=record];
            E [label="<c0> 0|<c1> 1",shape=record];
            B -> D:c0;
            B -> D:c1;
            C -> E:c0;
            C -> E:c1;
        }
        """)

.. gdot::
    :format: svg
    :script: AFTER-THIS

    print("before the graph")
    print("AFTER-THIS", """
    digraph tree {
        A [label="X1 &lt; 5",shape=record];
        B [label="X2 &lt; 3",shape=record];
        C [label="X3 &lt; 2",shape=record];
        A -> B;
        A -> C;
        D [label="<c0> 0|<c1> 1",shape=record];
        E [label="<c0> 0|<c1> 1",shape=record];
        B -> D:c0;
        B -> D:c1;
        C -> E:c0;
        C -> E:c1;
    }
    """)

Finally, the tag `:process:` can be used to run the script in
a separate process.

Directive
=========

.. autoclass:: sphinx_runpython.gdot.sphinx_gdot_extension.GDotDirective
