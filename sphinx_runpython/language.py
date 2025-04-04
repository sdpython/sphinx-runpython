TITLES = {
    "en": {
        "ado": "teen",
        "allblogs": "All blog posts",
        "author": "author",
        "blocref_node": "",
        "blog_entry": (
            "The original entry is located in <<%s>>, line %d and can be found "
        ),
        "blogpost": "blogpost",
        "book": "book",
        "brefmes": "(<<%s>> : %s, line %d)",
        "by category:": "By category:",
        "by month:": "By month:",
        "by title:": "By title :",
        "catsmaonths": "All categories and months",
        "changes": "Changes",
        "child": "child",
        "cmdmes": "(<<%s>> : %s, line %d)",
        "code": "code",
        "comic": "comic",
        "disc": "disc",
        "download": "download",
        "exmes": "(<<%s>> : %s, line %d)",
        "exref_node": "Examples",
        "FAQ": "FAQ",
        "faqmes": "(<<%s>> : %s, line %d)",
        "faqref_node": "FAQ",
        "film": "movie",
        "glossary": "Glossary",
        "hide": "hide",
        "In": "<<<",
        "license": "License",
        "Magic commands": "Magic commands",
        "main": "blog list",
        "main2": "blog main page",
        "main_title": "blog page",
        "manga": "manga",
        "mathdef_node": "",
        "mathmes": "(<<%s>> : %s, line %d)",
        "more": "post",
        "nbmes": "(<<%s>> : %s, line %d)",
        "nbref_node": "Magic command",
        "original entry": "original entry",
        "Out": ">>>",
        "Out2": "Raw",
        "outl": "output",
        "page1": "first page",
        "show": "show",
        "toc": "Contents",
        "toc0": "Links",
        "toc1": "Information",
        "todo": "Todo",
        "todo_node": "Todo",
        "todoext_node": "",
        "todomes": "(The <<%s>> is located in %s, line %d.)",
        "unhide": "unhide",
    },
    "fr": {
        "ado": "ado",
        "allblogs": "Tous les articles de blog",
        "author": "auteur",
        "blocref_node": "",
        "blog_entry": "Source <<%s>>, line %d and can be found ",
        "blogpost": "article",
        "book": "livre",
        "brefmes": "(<<%s>> : %s, ligne %d)",
        "by category:": "Par catégorie :",
        "by month:": "Par mois :",
        "by title:": "Par titre :",
        "catsmaonths": "Catégories et mois",
        "changes": "Changements",
        "child": "enfant",
        "cmdmes": "(<<%s>> : %s, line %d)",
        "code": "code",
        "comic": "bande dessinée",
        "disc": "disque",
        "download": "télécharger",
        "exmes": "(<<%s>> : %s, ligne %d)",
        "exref_node": "Exemples",
        "FAQ": "FAQ",
        "faqmes": "(<<%s>> : %s, ligne %d)",
        "faqref_node": "FAQ",
        "film": "film",
        "glossary": "Glossaire",
        "hide": "cacher",
        "In": "<<<",
        "license": "Licence",
        "Magic commands": "Commandes magiques",
        "main": "liste d'articles du blog",
        "main2": "page principale du blog",
        "main_title": "page de blog",
        "manga": "dessin animé",
        "mathdef_node": "",
        "mathmes": "(<<%s>> : %s, ligne %d)",
        "more": "article",
        "nbmes": "(<<%s>> : %s, ligne %d)",
        "nbref_node": "Commande magique",
        "original entry": "source",
        "Out": ">>>",
        "Out2": "Sortie brute",
        "outl": "la sortie",
        "page1": "première page",
        "show": "série",
        "toc": "Contenu",
        "toc0": "Liens",
        "toc1": "Information",
        "todo": "A faire",
        "todo_node": "A faire",
        "todoext_node": "",
        "todomes": "(<<%s>> : %s, ligne %d)",
        "unhide": "montrer",
    },
}


def sphinx_lang(env, default_value="en"):
    """
    Returns the language defined in the configuration file.

    :param env: environment
    :param default_value: default value
    :return: language
    """
    if hasattr(env, "settings"):
        settings = env.settings
        if hasattr(settings, "language_code"):
            lang = env.settings.language_code
        else:
            lang = "en"
    else:
        settings = None
        lang = "en"
    return lang
