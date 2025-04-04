from docutils import nodes
from docutils.parsers.rst import directives

import sphinx
from sphinx.locale import _
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.statemachine import StringList
from sphinx.util.nodes import nested_parse_with_titles
from ..language import TITLES


class quote_node(nodes.admonition):
    """
    Defines ``quote`` node.
    """

    pass


class QuoteNode(BaseAdmonition):
    """
    A ``quotedef`` entry, displayed in the form of an admonition.
    It takes the following options:

    * *author*
    * *book* or *manga* or *film* or *show* or *disc* or
      *comic* or *child* or *ado*
    * *year*
    * *pages*
    * *tag*
    * *source*
    * *lid* or *label*
    * *index*, additional index words beside the title and the author
    * *date*, if the text was written or declared at specific date
    * *title1*, by default, the author comes first, if True, the title is

    Example::

        .. quote::
            :author: author
            :book: book
            :year: year
            :pages: pages (optional)
            :tag: something
            :lid: id (used for further reference)
            :source: optional
            :index: word

            A monkey could...
    """

    node_class = quote_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "author": directives.unchanged,
        "book": directives.unchanged,
        "manga": directives.unchanged,
        "disc": directives.unchanged,
        "ado": directives.unchanged,
        "child": directives.unchanged,
        "comic": directives.unchanged,
        "show": directives.unchanged,
        "film": directives.unchanged,
        "year": directives.unchanged,
        "pages": directives.unchanged,
        "tag": directives.unchanged,
        "lid": directives.unchanged,
        "label": directives.unchanged,
        "source": directives.unchanged,
        "class": directives.class_option,
        "index": directives.unchanged,
        "date": directives.unchanged,
        "title1": directives.unchanged,
    }

    def run(self):
        """
        Builds the mathdef text.
        """
        env = (
            self.state.document.settings.env
            if hasattr(self.state.document.settings, "env")
            else None
        )
        docname = None if env is None else env.docname
        if docname is not None:
            docname = docname.replace("\\", "/").split("/")[-1]
        language_code = (
            self.state.document.settings.language_code
            if hasattr(self.state.document.settings, "language_code")
            else "en"
        )

        if not self.options.get("class"):
            self.options["class"] = ["admonition-quote"]

        # body
        (quote,) = super(QuoteNode, self).run()  # noqa: UP008
        if isinstance(quote, nodes.system_message):
            return [quote]

        # mid
        tag = self.options.get("tag", "quotetag").strip()
        if len(tag) == 0:
            raise ValueError("tag is empty")

        def __(text):
            if text:
                return _(text)
            return ""

        # book
        author = __(self.options.get("author", "").strip())
        book = __(self.options.get("book", "").strip())
        manga = __(self.options.get("manga", "").strip())
        comic = __(self.options.get("comic", "").strip())
        ado = __(self.options.get("ado", "").strip())
        child = __(self.options.get("child", "").strip())
        disc = __(self.options.get("disc", "").strip())
        film = __(self.options.get("film", "").strip())
        show = __(self.options.get("show", "").strip())
        pages = __(self.options.get("pages", "").strip())
        year = __(self.options.get("year", "").strip())
        source = __(self.options.get("source", "").strip())
        index = __(self.options.get("index", "").strip())
        date = __(self.options.get("date", "").strip())
        title1 = __(self.options.get("title1", "").strip()) in (
            "1",
            1,
            "True",
            True,
            "true",
        )

        indexes = []
        if index:
            indexes.append(index)

        # add a label
        lid = self.options.get("lid", self.options.get("label", None))
        if lid:
            tnl = ["", f".. _{lid}:", ""]
        else:
            tnl = []

        if title1:
            if ado:
                tnl.append(f"**{ado}**")
            if child:
                tnl.append(f"**{child}**")
            if comic:
                tnl.append(f"**{comic}**")
            if disc:
                tnl.append(f"**{disc}**")
            if book:
                tnl.append(f"**{book}**")
            if manga:
                tnl.append(f"**{manga}**")
            if show:
                tnl.append(f"**{show}**")
            if film:
                tnl.append(f"**{film}**")
            if author:
                tnl.append(f"*{author}*, ")
        else:
            if author:
                tnl.append(f"**{author}**, ")
            if ado:
                tnl.append(f"*{ado}*")
            if child:
                tnl.append(f"*{child}*")
            if comic:
                tnl.append(f"*{comic}*")
            if disc:
                tnl.append(f"*{disc}*")
            if book:
                tnl.append(f"*{book}*")
            if manga:
                tnl.append(f"*{manga}*")
            if show:
                tnl.append(f"*{show}*")
            if film:
                tnl.append(f"*{film}*")

        if author:
            indexes.append(author)
            indexes.append(TITLES[language_code]["author"] + "; " + author)
        if ado:
            indexes.append(ado)
            indexes.append(TITLES[language_code]["ado"] + "; " + ado)
        if child:
            indexes.append(child)
            indexes.append(TITLES[language_code]["child"] + "; " + child)
        if comic:
            indexes.append(comic)
            indexes.append(TITLES[language_code]["comic"] + "; " + comic)
        if disc:
            indexes.append(disc)
            indexes.append(TITLES[language_code]["disc"] + "; " + disc)
        if book:
            indexes.append(book)
            indexes.append(TITLES[language_code]["book"] + "; " + book)
        if manga:
            indexes.append(manga)
            indexes.append(TITLES[language_code]["manga"] + "; " + manga)
        if show:
            indexes.append(show)
            indexes.append(TITLES[language_code]["show"] + "; " + show)
        if film:
            indexes.append(film)
            indexes.append(TITLES[language_code]["film"] + "; " + film)

        if pages:
            tnl.append(f", {pages}")
        if date:
            tnl.append(f"({date})")
        if year:
            tnl.append(f"({year})")
        if source:
            if source.startswith("http"):
                tnl.append(f", `source <{source}>`__")
            else:
                tnl.append(f", {source}")
        tnl.append("")
        tnl.append(".. index:: " + ", ".join(indexes))
        tnl.append("")

        content = StringList(tnl)
        content = content + self.content
        node = quote_node()

        try:
            nested_parse_with_titles(self.state, content, node)
        except Exception as e:
            from sphinx.util import logging

            logger = logging.getLogger("blogpost")
            logger.warning(
                "[blogpost] unable to parse %r - %r - %r", author, book or manga, e
            )
            raise e

        node["tag"] = tag
        node["author"] = author
        node["pages"] = pages
        node["year"] = year
        node["label"] = lid
        node["source"] = source
        node["book"] = book
        node["manga"] = manga
        node["disc"] = disc
        node["comic"] = comic
        node["ado"] = ado
        node["child"] = child
        node["film"] = film
        node["show"] = show
        node["index"] = index
        node["content"] = "\n".join(self.content)
        node["classes"] += ["quote"]

        return [node]


def visit_quote_node(self, node):
    """
    visit_quote_node
    """
    self.visit_admonition(node)


def depart_quote_node(self, node):
    """
    depart_quote_node,
    see https://github.com/sphinx-doc/sphinx/blob/master/sphinx/writers/html.py
    """
    self.depart_admonition(node)


def visit_quote_node_rst(self, node):
    """
    visit_quote_node
    """
    self.new_state(0)
    self.add_text(".. quote::")
    for k, v in sorted(node.attributes.items()):
        if k in ("content", "classes"):
            continue
        if v:
            self.new_state(4)
            self.add_text(f":{k}: {v}")
            self.end_state(wrap=False, end=None)
    self.add_text(self.nl)
    self.new_state(4)
    self.add_text(node["content"])
    self.end_state()
    self.end_state()
    raise nodes.SkipNode


def depart_quote_node_rst(self, node):
    """
    depart_quote_node,
    see https://github.com/sphinx-doc/sphinx/blob/master/sphinx/writers/html.py
    """
    pass


def setup(app):
    """
    setup for ``mathdef`` (sphinx)
    """
    if hasattr(app, "add_mapping"):
        app.add_mapping("quote", quote_node)

    app.add_node(
        quote_node,
        html=(visit_quote_node, depart_quote_node),
        epub=(visit_quote_node, depart_quote_node),
        elatex=(visit_quote_node, depart_quote_node),
        latex=(visit_quote_node, depart_quote_node),
        text=(visit_quote_node, depart_quote_node),
        md=(visit_quote_node, depart_quote_node),
        rst=(visit_quote_node_rst, depart_quote_node_rst),
    )

    app.add_directive("quote", QuoteNode)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
