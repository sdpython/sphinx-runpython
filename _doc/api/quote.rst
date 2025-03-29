=====
quote
=====

A block to insert a quote from a book, a film...

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
        :source: https://sdpython.github.io/doc/sphinx-runpython/dev/

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

Another example:

::

    .. quote::
        :author: René Descartes
        :book: Discours de la méthode
        :index: philosophie
        :year: 1637
        :title1: true
        :source: https://fr.wikipedia.org/wiki/Discours_de_la_m%C3%A9thode

        Je l'ai lu à une époque où je ne détestais pas la lecture,
        ni la philosophie sans pour autant que l'une des deux m'attire.
        Et j'ai adoré ce livre, peut-être parce qu'il était écrit par
        un mathématicien, peut-être aussi parce que l'auteur met en évidence
        ce qu'il sait, ce qu'il ne sait pas et ce qu'il en déduit.
        Je n'aimais pas à l'époque qu'un sujet aboutissent à des
        conclusions différentes quand il était abordé par des auteurs
        différents. Descartes ne laissait pas de place à l'ambiguïté.
        J'ai retenu que chacun avait sa façon de voir et comprendre le monde
        et qu'il n'était pas évident que nous puissions trouver un moyen
        commun d'échanger nos idées et que de fait celui-ci n'existait pas
        car il était difficile de vérifier que les mêmes mots eussent le même sens.
        J'en déduis qu'il était prévisible que deux philosophes puissent
        avoir des avis contraires. Ils ne parlaient pas le même language.

    .. quote::
        :author: Agatha Christie
        :book: Une poignée de seigle
        :year: 1953
        :index: problème
        :source: https://fr.wikipedia.org/wiki/Une_poign%C3%A9e_de_seigle
        :pages: 173

        Un problème n'est pas résolu quand on lui a donné une solution
        boiteuse. C'est Kipling qui a dit ça. On ne lit plus Kipling,
        mais c'était un grand homme.

.. quote::
    :author: René Descartes
    :book: Discours de la méthode
    :index: philosophie
    :year: 1637
    :title1: true
    :source: https://fr.wikipedia.org/wiki/Discours_de_la_m%C3%A9thode

    Je l'ai lu à une époque où je ne détestais pas la lecture,
    ni la philosophie sans pour autant que l'une des deux m'attire.
    Et j'ai adoré ce livre, peut-être parce qu'il était écrit par
    un mathématicien, peut-être aussi parce que l'auteur met en évidence
    ce qu'il sait, ce qu'il ne sait pas et ce qu'il en déduit.
    Je n'aimais pas à l'époque qu'un sujet aboutissent à des
    conclusions différentes quand il était abordé par des auteurs
    différents. Descartes ne laissait pas de place à l'ambiguïté.
    J'ai retenu que chacun avait sa façon de voir et comprendre le monde
    et qu'il n'était pas évident que nous puissions trouver un moyen
    commun d'échanger nos idées et que de fait celui-ci n'existait pas
    car il était difficile de vérifier que les mêmes mots eussent le même sens.
    J'en déduis qu'il était prévisible que deux philosophes puissent
    avoir des avis contraires. Ils ne parlaient pas le même language.

.. quote::
    :author: Agatha Christie
    :book: Une poignée de seigle
    :year: 1953
    :index: problème
    :source: https://fr.wikipedia.org/wiki/Une_poign%C3%A9e_de_seigle
    :pages: 173

    Un problème n'est pas résolu quand on lui a donné une solution
    boiteuse. C'est Kipling qui a dit ça. On ne lit plus Kipling,
    mais c'était un grand homme.

Directive
=========

.. autoclass:: sphinx_runpython.quote.sphinx_quote_extension.QuoteNode
