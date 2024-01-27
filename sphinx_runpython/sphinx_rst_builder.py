"""
It is inspired from `restbuilder
<https://github.com/sphinx-contrib/legacy>`_.
I replicate its license here:

::

    Copyright (c) 2012-2013 by Freek Dijkstra <software@macfreek.nl>.
    Some rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import hashlib
import glob
import os
import re
import textwrap
import shutil
import sys
import urllib.request
from docutils.io import StringOutput
from docutils import nodes, writers
from sphinx.util import logging
from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir

# from sphinx.locale import admonitionlabels, _
try:
    from sphinx.domains.changeset import versionlabels
except ImportError:  # pragma: no cover
    from sphinx.locale import versionlabels
from sphinx.writers.text import TextTranslator, MAXWIDTH, STDINDENT

from .ext_io_helper import InternetException, get_url_content_timeout


class CommonSphinxWriterHelpers:
    """
    Common functions used in @see cl RstTranslator
    and @see cl MdTranslator.
    """

    def hash_md5_readfile(self, filename: str) -> str:
        """
        Computes a hash of a file.
        :param filename: filename
        :return: string
        """
        with open(filename, "rb") as f:
            m = hashlib.md5()
            readBytes = 1024**2  # read 1024 bytes per time
            totalBytes = 0
            while readBytes:
                readString = f.read(readBytes)
                m.update(readString)
                readBytes = len(readString)
                totalBytes += readBytes
        res = m.hexdigest()
        if len(res) > 20:
            res = res[:20]
        return res

    def base_visit_image(self, node, image_dest=None):
        """
        Processes an image. By default, it writes the image on disk.
        Inspired from
        `visit_image
        <https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/html4css1/__init__.py#L1019>`_
        implemented in :epkg:`docutils`.

        :param node: image node
        :param image_dest: image destination (location where they will be copied)
        :return: attributes
        """
        atts = {}
        uri = node["uri"]

        # place SVG and SWF images in an <object> element
        types = {".svg": "image/svg+xml", ".swf": "application/x-shockwave-flash"}
        ext = os.path.splitext(uri)[1].lower()
        if ext in (".svg", ".swf"):
            atts["data"] = uri
            atts["type"] = types[ext]

        atts["src"] = uri
        atts["alt"] = node.get("alt", uri)

        env = self.builder.env  # pylint: disable=E1101
        if hasattr(env, "remote_images") and atts["src"] in env.remote_images:
            atts["src"] = env.remote_images[atts["src"]]

        # Makes a local copy of the image
        if "src" in atts:
            builder = self.builder  # pylint: disable=E1101
            srcdir = builder.srcdir
            if srcdir == "IMPOSSIBLE:TOFIND":
                srcdir = None
            if image_dest is None:
                outdir = builder.outdir
                if builder.current_docname and builder.current_docname != "<<string>>":
                    if srcdir is None:
                        current = os.path.dirname(builder.current_docname)
                    else:
                        current = os.path.dirname(
                            os.path.join(srcdir, builder.current_docname)
                        )
                    if current is None or not os.path.exists(current):
                        raise FileNotFoundError(  # pragma: no cover
                            "Unable to find document '{0}' current_docname='{1}'"
                            "".format(current, builder.current_docname)
                        )
                    dest = os.path.dirname(
                        os.path.join(outdir, builder.current_docname)
                    )
                    fold = outdir
                else:
                    # current_docname is None which means
                    # no file should be created
                    fold = None
            else:
                fold = image_dest

            if atts["src"].startswith("http:") or atts["src"].startswith("https:"):
                name = hashlib.sha1(atts["src"].encode()).hexdigest()
                ext = os.path.splitext(atts["src"])[-1]
                remote = True
            else:
                full = os.path.join(srcdir, atts["src"]) if srcdir else atts["src"]

                if "*" in full:
                    files = glob.glob(full)
                    if len(files) == 0:
                        raise FileNotFoundError(  # pragma: no cover
                            f"Unable to find any file matching pattern '{full}'."
                        )
                    full = files[0]

                if not os.path.exists(full):
                    this = os.path.abspath(os.path.dirname(__file__))
                    repl = os.path.join(
                        this, "sphinximages", "sphinxtrib", "missing.png"
                    )
                    logger = logging.getLogger("image")
                    logger.warning(
                        "[image] unable to find image %r, replaced by %r.", full, repl
                    )
                    full = repl

                ext = os.path.splitext(full)[-1]
                name = self.hash_md5_readfile(full) + ext
                remote = False

            if fold is not None and not os.path.exists(fold):
                os.makedirs(fold)

            dest = os.path.join(fold, name) if fold else None
            if dest is not None and "*" in dest:
                raise RuntimeError(  # pragma: no cover
                    "Wrong destination '{} // {}' image_dest='{}' atts['src']='{}' "
                    "srcdir='{}' full='{}'.".format(
                        fold, name, image_dest, atts["src"], srcdir, full
                    )
                )

            if dest is not None:
                if not os.path.exists(dest):
                    if remote:
                        if atts.get("download", False):
                            # Downloads the image
                            try:
                                get_url_content_timeout(
                                    atts["src"], output=dest, encoding=None, timeout=20
                                )
                                full = atts["src"]
                            except InternetException as e:
                                logger = logging.getLogger("image")
                                logger.warning(
                                    "[image] unable to get content "
                                    "for url %r due to %r",
                                    atts["src"],
                                    e,
                                )
                                this = os.path.abspath(os.path.dirname(__file__))
                                full = os.path.join(
                                    this, "sphinximages", "sphinxtrib", "missing.png"
                                )
                                shutil.copy(full, dest)
                        else:
                            name = atts["src"]
                            full = name
                            dest = name
                    else:
                        if ":" in dest and len(dest) > 2:
                            dest = dest[:2] + dest[2:].replace(":", "_")
                            ext = os.path.splitext(dest)[-1]
                            if ext not in (".png", ".jpg"):
                                dest += ".png"
                        try:
                            shutil.copy(full, dest)
                        except (FileNotFoundError, OSError) as e:
                            raise FileNotFoundError(  # pragma: no cover
                                f"Unable to copy from '{full}' to '{dest}'."
                            ) from e
                        full = dest
                else:
                    full = dest
            else:
                name = atts["src"]
                full = name
                dest = name

            atts["src"] = name
            atts["full"] = full
            atts["dest"] = dest
        else:
            raise ValueError(  # pragma: no cover
                "No image was found in node (class='{1}')\n{0}".format(
                    node, self.__class__.__name__
                )
            )

        # image size
        if "width" in node:
            atts["width"] = node["width"]
        if "height" in node:
            atts["height"] = node["height"]
        if "download" in node:
            atts["download"] = node["download"]
        if "scale" in node:
            import PIL

            if "width" not in node or "height" not in node:
                imagepath = urllib.request.url2pathname(uri)
                try:
                    img = PIL.Image.open(imagepath.encode(sys.getfilesystemencoding()))
                except (IOError, UnicodeEncodeError):  # pragma: no cover
                    pass  # TODO: warn?
                else:
                    self.settings.record_dependencies.add(  # pylint: disable=E1101
                        imagepath.replace("\\", "/")
                    )
                    if "width" not in atts:
                        atts["width"] = "%dpx" % img.size[0]
                    if "height" not in atts:
                        atts["height"] = "%dpx" % img.size[1]
            for att_name in "width", "height":
                if att_name in atts:
                    match = re.match(r"([0-9.]+)(\S*)$", atts[att_name])
                    atts[att_name] = "%s%s" % (
                        float(match.group(1)) * (float(node["scale"]) / 100),
                        match.group(2),
                    )

        style = []
        for att_name in "width", "height":
            if att_name in atts:
                if re.match(r"^[0-9.]+$", atts[att_name]):
                    # Interpret unitless values as pixels.
                    atts[att_name] += "px"
                style.append(f"{att_name}: {atts[att_name]};")

        if style:
            atts["style"] = " ".join(style)

        if "align" in node:
            atts["class"] = f"align-{node['align']}"

        return atts


class RstTranslator(TextTranslator, CommonSphinxWriterHelpers):
    """
    Defines a :epkg:`RST` translator.
    """

    sectionchars = '*=-~"+`'

    def __init__(self, document, builder):
        if not hasattr(builder, "config"):
            raise TypeError(f"Builder has no config: {type(builder)}")
        TextTranslator.__init__(self, document, builder)

        newlines = builder.config.text_newlines
        if newlines == "windows":
            self.nl = "\r\n"
        elif newlines == "native":
            self.nl = os.linesep
        else:
            self.nl = "\n"
        self.sectionchars = builder.config.text_sectionchars
        self.states = [[]]
        self.stateindent = [0]
        self.list_counter = []
        self.sectionlevel = 0
        self._table = None
        if self.builder.config.rst_indent:
            self.indent = self.builder.config.rst_indent
        else:
            self.indent = STDINDENT
        self.wrapper = textwrap.TextWrapper(
            width=STDINDENT, break_long_words=False, break_on_hyphens=False
        )

    def log_unknown(self, type, node):
        logger = logging.getLogger("RstBuilder")
        logger.warning("[rst] %s(%s) unsupported formatting", type, node)

    def wrap(self, text, width=STDINDENT):
        self.wrapper.width = width
        return self.wrapper.wrap(text)

    def add_text(self, text, indent=-1):
        self.states[-1].append((indent, text))

    def new_state(self, indent=STDINDENT):
        self.states.append([])
        self.stateindent.append(indent)

    def end_state(self, wrap=True, end=[""], first=None):
        content = self.states.pop()
        maxindent = sum(self.stateindent)
        indent = self.stateindent.pop()
        result = []
        toformat = []

        def do_format():
            if not toformat:
                return
            if wrap:
                res = self.wrap("".join(toformat), width=MAXWIDTH - maxindent)
            else:
                res = "".join(toformat).splitlines()
            if end:
                res += end
            result.append((indent, res))

        for itemindent, item in content:
            if itemindent == -1:
                toformat.append(item)
            else:
                do_format()
                result.append((indent + itemindent, item))
                toformat = []

        do_format()

        if first is not None and result:
            itemindent, item = result[0]
            if item:
                result.insert(0, (itemindent - indent, [first + item[0]]))
                result[1] = (itemindent, item[1:])

        self.states[-1].extend(result)

    def visit_document(self, node):
        self.new_state(0)

    def depart_document(self, node):
        self.end_state()
        self.body = self.nl.join(
            line and (" " * indent + line)
            for indent, lines in self.states[0]
            for line in lines
        )

    def visit_highlightlang(self, node):
        raise nodes.SkipNode

    def visit_section(self, node):
        self._title_char = self.sectionchars[self.sectionlevel]
        self.sectionlevel += 1

    def depart_section(self, node):
        self.sectionlevel -= 1

    def visit_topic(self, node):
        self.new_state(0)

    def depart_topic(self, node):
        self.end_state()

    visit_sidebar = visit_topic
    depart_sidebar = depart_topic

    def visit_rubric(self, node):
        self.new_state(0)
        self.add_text("-[ ")

    def depart_rubric(self, node):
        self.add_text(" ]-")
        self.end_state()

    def visit_compound(self, node):
        # self.log_unknown("compount", node)
        pass

    def depart_compound(self, node):
        pass

    def visit_glossary(self, node):
        # self.log_unknown("glossary", node)
        pass

    def depart_glossary(self, node):
        pass

    def visit_title(self, node):
        if isinstance(node.parent, nodes.Admonition):
            self.add_text(node.astext() + ": ")
            raise nodes.SkipNode
        self.new_state(0)

    def depart_title(self, node):
        if isinstance(node.parent, nodes.section):
            char = self._title_char
        else:
            char = "^"
        text = "".join(x[1] for x in self.states.pop() if x[0] == -1)
        self.stateindent.pop()
        self.states[-1].append((0, ["", text, f"{char * len(text)}", ""]))

    def visit_subtitle(self, node):
        # self.log_unknown("subtitle", node)
        pass

    def depart_subtitle(self, node):
        pass

    def visit_attribution(self, node):
        self.add_text("-- ")

    def depart_attribution(self, node):
        pass

    def visit_desc(self, node):
        self.new_state(0)

    def depart_desc(self, node):
        self.end_state()

    def visit_desc_signature(self, node):
        if node.parent["objtype"] in ("class", "exception", "method", "function"):
            self.add_text("**")
        else:
            self.add_text("``")

    def depart_desc_signature(self, node):
        if node.parent["objtype"] in ("class", "exception", "method", "function"):
            self.add_text("**")
        else:
            self.add_text("``")

    def visit_desc_name(self, node):
        # self.log_unknown("desc_name", node)
        pass

    def depart_desc_name(self, node):
        pass

    def visit_desc_addname(self, node):
        # self.log_unknown("desc_addname", node)
        pass

    def depart_desc_addname(self, node):
        pass

    def visit_desc_type(self, node):
        # self.log_unknown("desc_type", node)
        pass

    def depart_desc_type(self, node):
        pass

    def visit_desc_returns(self, node):
        self.add_text(" -> ")

    def depart_desc_returns(self, node):
        pass

    def visit_desc_parameterlist(self, node):
        self.add_text("(")
        self.first_param = 1

    def depart_desc_parameterlist(self, node):
        self.add_text(")")

    def visit_desc_parameter(self, node):
        if not self.first_param:
            self.add_text(", ")
        else:
            self.first_param = 0
        self.add_text(node.astext())
        raise nodes.SkipNode

    def visit_desc_optional(self, node):
        self.add_text("[")

    def depart_desc_optional(self, node):
        self.add_text("]")

    def visit_desc_annotation(self, node):
        content = node.astext()
        if len(content) > MAXWIDTH:  # pragma: no cover
            h = int(MAXWIDTH / 3)
            content = content[:h] + " ... " + content[-h:]
            self.add_text(content)
            raise nodes.SkipNode

    def depart_desc_annotation(self, node):
        pass

    def visit_refcount(self, node):
        pass

    def depart_refcount(self, node):
        pass

    def visit_desc_content(self, node):
        self.new_state(self.indent)

    def depart_desc_content(self, node):
        self.end_state()

    def visit_figure(self, node):
        self.new_state(self.indent)

    def depart_figure(self, node):
        self.end_state()

    def visit_caption(self, node):
        # self.log_unknown("caption", node)
        pass

    def depart_caption(self, node):
        pass

    def visit_productionlist(self, node):
        self.new_state(self.indent)
        names = []
        for production in node:
            names.append(production["tokenname"])
        maxlen = max(len(name) for name in names)
        for production in node:
            if production["tokenname"]:
                self.add_text(production["tokenname"].ljust(maxlen) + " ::=")
                lastname = production["tokenname"]
            else:
                self.add_text(f"{' ' * len(lastname)}    ")
            self.add_text(production.astext() + self.nl)
        self.end_state(wrap=False)
        raise nodes.SkipNode

    def visit_seealso(self, node):
        self.new_state(self.indent)

    def depart_seealso(self, node):
        self.end_state(first="")

    def visit_footnote(self, node):
        self._footnote = node.children[0].astext().strip()
        self.new_state(len(self._footnote) + self.indent)

    def depart_footnote(self, node):
        self.end_state(first=f"[{self._footnote}] ")

    def visit_citation(self, node):
        if len(node) and isinstance(node[0], nodes.label):
            self._citlabel = node[0].astext()
        else:
            self._citlabel = ""
        self.new_state(len(self._citlabel) + self.indent)

    def depart_citation(self, node):
        self.end_state(first=f"[{self._citlabel}] ")

    def visit_label(self, node):
        raise nodes.SkipNode

    def visit_option_list(self, node):
        # self.log_unknown("option_list", node)
        pass

    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        self.new_state(0)

    def depart_option_list_item(self, node):
        self.end_state()

    def visit_option_group(self, node):
        self._firstoption = True

    def depart_option_group(self, node):
        self.add_text("     ")

    def visit_option(self, node):
        if self._firstoption:
            self._firstoption = False
        else:
            self.add_text(", ")

    def depart_option(self, node):
        pass

    def visit_option_string(self, node):
        # self.log_unknown("option_string", node)
        pass

    def depart_option_string(self, node):
        pass

    def visit_option_argument(self, node):
        self.add_text(node["delimiter"])

    def depart_option_argument(self, node):
        pass

    def visit_description(self, node):
        # self.log_unknown("description", node)
        pass

    def depart_description(self, node):
        pass

    def visit_tabular_col_spec(self, node):
        raise nodes.SkipNode

    def visit_colspec(self, node):
        self._table[0].append(node["colwidth"])
        raise nodes.SkipNode

    def visit_tgroup(self, node):
        # self.log_unknown("tgroup", node)
        pass

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        # self.log_unknown("thead", node)
        pass

    def depart_thead(self, node):
        pass

    def visit_tbody(self, node):
        self._table.append("sep")

    def depart_tbody(self, node):
        pass

    def visit_row(self, node):
        self._table.append([])

    def depart_row(self, node):
        pass

    def visit_entry(self, node):
        if hasattr(node, "morerows") or hasattr(node, "morecols"):
            raise NotImplementedError(
                "Column or row spanning cells are " "not implemented."
            )
        self.new_state(0)

    def depart_entry(self, node):
        text = self.nl.join(self.nl.join(x[1]) for x in self.states.pop())
        self.stateindent.pop()
        self._table[-1].append(text)

    def visit_table(self, node):
        if self._table:
            raise NotImplementedError("Nested tables are not supported.")
        self.new_state(0)
        self._table = [[]]

    def depart_table(self, node):
        lines = self._table[1:]
        fmted_rows = []
        colwidths = self._table[0]
        realwidths = list(map(lambda x: x if isinstance(x, int) else 1, colwidths[:]))
        separator = 0
        # don't allow paragraphs in table cells for now
        for line in lines:
            if line == "sep":
                separator = len(fmted_rows)
            else:
                cells = []
                for i, cell in enumerate(line):
                    try:
                        par = self.wrap(cell, width=int(colwidths[i]))
                    except (IndexError, ValueError):
                        par = self.wrap(cell)
                    if par:
                        maxwidth = max(map(len, par))
                    else:
                        maxwidth = 0
                    if i >= len(realwidths):
                        realwidths.append(maxwidth)
                    elif isinstance(realwidths[i], str):
                        realwidths[i] = maxwidth
                    else:
                        realwidths[i] = max(realwidths[i], maxwidth)
                    cells.append(par)
                fmted_rows.append(cells)
        self._table = None

        def writesep(char="-"):
            out = ["+"]
            for width in realwidths:
                out.append(char * (width + 2))
                out.append("+")
            self.add_text("".join(out) + self.nl)

        def writerow(row):
            lines = zip(*row)
            for line in lines:
                out = ["|"]
                for i, cell in enumerate(line):
                    if cell:
                        out.append(" " + cell.ljust(realwidths[i] + 1))
                    else:
                        out.append(" " * (realwidths[i] + 2))
                    out.append("|")
                self.add_text("".join(out) + self.nl)

        for i, row in enumerate(fmted_rows):
            if separator and i == separator:
                writesep("=")
            else:
                writesep("-")
            writerow(row)
        writesep("-")
        self._table = None
        self.end_state(wrap=False)

    def visit_acks(self, node):
        self.new_state(0)
        self.add_text(", ".join(n.astext() for n in node.children[0].children) + ".")
        self.end_state()
        raise nodes.SkipNode

    def visit_simpleimage(self, node):
        self.visit_image(node)

    def depart_simpleimage(self, node):
        self.depart_image(node)

    def visit_image(self, node):
        self.new_state(0)
        atts = self.base_visit_image(node, self.builder.rst_image_dest)
        self.add_text(f".. image:: {atts['src']}")
        for att_name in "width", "height", "alt", "download":
            if att_name in node.attributes and node.get(att_name) != "auto":
                self.new_state(4)
                self.add_text(f":{att_name}: {node[att_name]}")
                self.end_state(wrap=False, end=None)

    def depart_image(self, node):
        self.end_state(wrap=False, end=None)

    def visit_transition(self, node):
        indent = sum(self.stateindent)
        self.new_state(0)
        self.add_text("=" * (MAXWIDTH - indent))
        self.end_state()
        raise nodes.SkipNode

    def visit_bullet_list(self, node):
        self.list_counter.append(-1)

    def depart_bullet_list(self, node):
        self.list_counter.pop()

    def visit_enumerated_list(self, node):
        self.list_counter.append(0)

    def depart_enumerated_list(self, node):
        self.list_counter.pop()

    def visit_definition_list(self, node):
        self.list_counter.append(-2)

    def depart_definition_list(self, node):
        self.list_counter.pop()

    def visit_list_item(self, node):
        if self.list_counter[-1] == -1:
            # bullet list
            self.new_state(self.indent)
        elif self.list_counter[-1] == -2:
            # definition list
            pass
        else:
            # enumerated list
            self.list_counter[-1] += 1
            self.new_state(len(str(self.list_counter[-1])) + self.indent)

    def depart_list_item(self, node):
        if self.list_counter[-1] == -1:
            self.end_state(first="* ", end=None)
        elif self.list_counter[-1] == -2:
            pass
        else:
            self.end_state(first=f"{self.list_counter[-1]}. ", end=None)

    def visit_definition_list_item(self, node):
        self._li_has_classifier = len(node) >= 2 and isinstance(
            node[1], nodes.classifier
        )

    def depart_definition_list_item(self, node):
        pass

    def visit_term(self, node):
        self.new_state(0)

    def depart_term(self, node):
        if not self._li_has_classifier:
            self.end_state(end=None)

    def visit_termsep(self, node):
        self.add_text(", ")
        raise nodes.SkipNode

    def visit_classifier(self, node):
        self.add_text(" : ")

    def depart_classifier(self, node):
        self.end_state(end=None)

    def visit_definition(self, node):
        self.new_state(self.indent)

    def depart_definition(self, node):
        self.end_state()

    def visit_field_list(self, node):
        # self.log_unknown("field_list", node)
        pass

    def depart_field_list(self, node):
        pass

    def visit_field(self, node):
        self.new_state(0)

    def depart_field(self, node):
        self.end_state(end=None)

    def visit_field_name(self, node):
        self.add_text(":")

    def depart_field_name(self, node):
        self.add_text(":")
        content = node.astext()
        self.add_text((16 - len(content)) * " ")

    def visit_field_body(self, node):
        self.new_state(self.indent)

    def depart_field_body(self, node):
        self.end_state()

    def visit_centered(self, node):
        pass

    def depart_centered(self, node):
        pass

    def visit_hlist(self, node):
        # self.log_unknown("hlist", node)
        pass

    def depart_hlist(self, node):
        pass

    def visit_hlistcol(self, node):
        # self.log_unknown("hlistcol", node)
        pass

    def depart_hlistcol(self, node):
        pass

    def visit_admonition(self, node):
        self.new_state(0)

    def depart_admonition(self, node):
        self.end_state()

    def _visit_admonition(self, node):
        self.new_state(self.indent)

    def _make_depart_admonition(name):
        def depart_admonition(self, node):
            self.end_state(first=name + ": ")

        return depart_admonition

    visit_attention = _visit_admonition
    depart_attention = _make_depart_admonition("attention")
    visit_caution = _visit_admonition
    depart_caution = _make_depart_admonition("caution")
    visit_danger = _visit_admonition
    depart_danger = _make_depart_admonition("danger")
    visit_error = _visit_admonition
    depart_error = _make_depart_admonition("error")
    visit_hint = _visit_admonition
    depart_hint = _make_depart_admonition("hint")
    visit_important = _visit_admonition
    depart_important = _make_depart_admonition("important")
    visit_note = _visit_admonition
    depart_note = _make_depart_admonition("note")
    visit_tip = _visit_admonition
    depart_tip = _make_depart_admonition("tip")
    visit_warning = _visit_admonition
    depart_warning = _make_depart_admonition("warning")

    def visit_versionmodified(self, node):
        self.new_state(0)
        if node.children:
            self.add_text(versionlabels[node["type"]] % node["version"] + ": ")
        else:
            self.add_text(versionlabels[node["type"]] % node["version"] + ".")

    def depart_versionmodified(self, node):
        self.end_state()

    def visit_literal_block(self, node):
        if "language" in node.attributes:
            self.add_text(f".. code-block:: {node['language']}")
            if "linenos" in node.attributes:
                self.new_state(4)
                self.add_text(":linenos:")
                self.end_state(wrap=False)
        else:
            self.add_text("::")
        self.new_state(self.indent)

    def depart_literal_block(self, node):
        self.end_state(wrap=False)

    def visit_doctest_block(self, node):
        self.new_state(0)

    def depart_doctest_block(self, node):
        self.end_state(wrap=False)

    def visit_line_block(self, node):
        self.new_state(0)

    def depart_line_block(self, node):
        self.end_state(wrap=False)

    def visit_line(self, node):
        # self.log_unknown("line", node)
        pass

    def depart_line(self, node):
        pass

    def visit_block_quote(self, node):
        self.add_text("..")
        self.new_state(self.indent)

    def depart_block_quote(self, node):
        self.end_state()

    def visit_compact_paragraph(self, node):
        pass

    def depart_compact_paragraph(self, node):
        pass

    def visit_paragraph(self, node):
        if not isinstance(node.parent, nodes.Admonition) or isinstance(
            node.parent, addnodes.seealso
        ):
            self.new_state(0)

    def depart_paragraph(self, node):
        if not isinstance(node.parent, nodes.Admonition) or isinstance(
            node.parent, addnodes.seealso
        ):
            self.end_state()

    def visit_target(self, node):
        if "refid" in node:
            self.new_state(0)
            self.add_text(".. _" + node["refid"] + ":" + self.nl)

    def depart_target(self, node):
        if "refid" in node:
            self.end_state(wrap=False)

    def visit_index(self, node):
        raise nodes.SkipNode

    def visit_substitution_definition(self, node):
        raise nodes.SkipNode

    def visit_pending_xref(self, node):
        if node.get("refexplicit"):
            text = f":py:{node['reftype']}:`{node.astext()} <{node['reftarget']}>`"
        else:
            text = f":py:{node['reftype']}:`{node['reftarget']}`"
        self.add_text(text)
        raise nodes.SkipNode

    def depart_pending_xref(self, node):
        raise NotImplementedError("Error")

    def visit_reference(self, node):
        """
        Runs upon entering a reference.
        Because this class inherits from the TextTranslator class,
        regularly defined links, such as::

            `Some Text`_

            .. _Some Text: http://www.some_url.com

        were being written as plaintext. This included internal
        references defined in the standard rst way, such as::

            `Some Reference`

            .. _Some Reference:

            Some Title
            ----------

        To resolve this, if ``refuri`` is not included in the node (an
        internal, non-Sphinx-defined internal uri, the reference is
        left unchanged.

        If ``internal`` is not in the node (as for an external,
        non-Sphinx URI, the reference is rewritten as an inline link,
        e.g.::

            Some Text <http://www.some_url.com>`_

        If ``reftitle`` is in the node (as in a Sphinx-generated
        reference), the node is converted to an inline link.

        Finally, all other links are also converted to an inline link
        format.
        """

        def clean_refuri(uri):
            ext = os.path.splitext(uri)[-1]
            link = uri if ext != ".rst" else uri[:-4]
            return link

        if "refuri" not in node:
            if "name" in node.attributes:
                self.add_text(f"`{node['name']}`_")
            elif "refid" in node and node["refid"]:
                self.add_text(f":ref:`{node['refid']}`")
            else:
                self.log_unknown(type(node), node)
        elif "internal" not in node and "name" in node.attributes:
            self.add_text(f"`{node['name']} <{clean_refuri(node['refuri'])}>`_")
        elif "internal" not in node and "names" in node.attributes:
            anchor = node["names"][0] if len(node["names"]) > 0 else node["refuri"]
            self.add_text(f"`{anchor} <{clean_refuri(node['refuri'])}>`_")
        elif "reftitle" in node:
            # Include node as text, rather than with markup.
            # reST seems unable to parse a construct like ` ``literal`` <url>`_
            # Hence it reverts to the more simple `literal <url>`_
            name = node["name"] if "name" in node else node.astext()
            self.add_text(f"`{name} <{clean_refuri(node['refuri'])}>`_")
            # self.end_state(wrap=False)
        else:
            name = node["name"] if "name" in node else node.astext()
            self.add_text(f"`{name} <{node['refuri']}>`_")
        if "internal" in node:
            raise nodes.SkipNode

    def depart_reference(self, node):
        if "refuri" not in node:
            pass  # Don't add these anchors
        elif "internal" not in node:
            # Don't add external links (they are automatically added by the reST spec)
            pass
        elif "reftitle" in node:
            pass

    def visit_download_reference(self, node):
        self.log_unknown("download_reference", node)

    def depart_download_reference(self, node):
        pass

    def visit_emphasis(self, node):
        self.add_text("*")

    def depart_emphasis(self, node):
        self.add_text("*")

    def visit_literal_emphasis(self, node):
        self.add_text("*")

    def depart_literal_emphasis(self, node):
        self.add_text("*")

    def visit_strong(self, node):
        self.add_text("**")

    def depart_strong(self, node):
        self.add_text("**")

    def visit_abbreviation(self, node):
        self.add_text("")

    def depart_abbreviation(self, node):
        if node.hasattr("explanation"):
            self.add_text(f" ({node['explanation']})")

    def visit_title_reference(self, node):
        # self.log_unknown("title_reference", node)
        self.add_text("*")

    def depart_title_reference(self, node):
        self.add_text("*")

    def visit_literal(self, node):
        self.add_text("``")

    def depart_literal(self, node):
        self.add_text("``")

    def visit_subscript(self, node):
        self.add_text("_")

    def depart_subscript(self, node):
        pass

    def visit_superscript(self, node):
        self.add_text("^")

    def depart_superscript(self, node):
        pass

    def visit_footnote_reference(self, node):
        self.add_text(f"[{node.astext()}]")
        raise nodes.SkipNode

    def visit_citation_reference(self, node):
        self.add_text(f"[{node.astext()}]")
        raise nodes.SkipNode

    def visit_Text(self, node):
        self.add_text(node.astext())

    def depart_Text(self, node):
        pass

    def visit_generated(self, node):
        # self.log_unknown("generated", node)
        pass

    def depart_generated(self, node):
        pass

    def visit_inline(self, node):
        # self.log_unknown("inline", node)
        pass

    def depart_inline(self, node):
        pass

    def visit_problematic(self, node):
        self.add_text(">>")

    def depart_problematic(self, node):
        self.add_text("<<")

    def visit_system_message(self, node):
        self.new_state(0)
        self.add_text(f"<SYSTEM MESSAGE: {node.astext()}>")
        self.end_state()
        raise nodes.SkipNode

    def visit_comment(self, node):
        raise nodes.SkipNode

    def visit_meta(self, node):
        # only valid for HTML
        raise nodes.SkipNode

    def visit_raw(self, node):
        if "text" in node.get("format", "").split():
            self.add_text(node.astext())
        raise nodes.SkipNode

    def visit_issue(self, node):
        self.add_text(":issue:`")
        self.add_text(node["text"])

    def depart_issue(self, node):
        self.add_text("`")

    def eval_expr(self, expr):
        md = False
        rst = True
        html = False
        latex = False
        if not (rst or html or latex or md):
            raise ValueError("One of them should be True")  # pragma: no cover
        try:
            ev = eval(expr)
        except Exception as e:  # pragma: no cover
            raise ValueError(f"Unable to interpret expression '{expr}' due to {e}.")
        return ev

    def visit_only(self, node):
        ev = self.eval_expr(node.attributes["expr"])
        if ev:
            pass
        else:
            raise nodes.SkipNode

    def depart_only(self, node):
        ev = self.eval_expr(node.attributes["expr"])
        if ev:
            pass
        else:
            # The program should not necessarily be here.
            pass

    def visit_CodeNode(self, node):
        self.add_text(".. CodeNode." + self.nl)

    def depart_CodeNode(self, node):
        pass

    def visit_inheritance_diagram(self, node):
        self.new_state(0)
        self.add_text(f".. inheritance_diagram:: {node['content']}")

    def depart_inheritance_diagram(self, node):
        self.end_state(wrap=False, end=["\n"])

    def visit_todo_node(self, node):
        self.visit_admonition(node)

    def depart_todo_node(self, node):
        self.depart_admonition(node)

    def visit_imgsgnode(self, node):
        self.add_text(".. imgsgnode(visit).")

    def depart_imgsgnode(self, node):
        self.add_text(".. imgsgnode(depart).")

    def unknown_visit(self, node):
        classname = node.__class__.__name__
        if classname in {
            "JupyterKernelNode",
            "JupyterCellNode",
            "JupyterWidgetViewNode",
            "JupyterWidgetStateNode",
            "ThebeSourceNode",
            "ThebeOutputNode",
            "ThebeButtonNode",
        }:
            # due to jupyter_sphinx
            return
        logger = logging.getLogger("RstBuilder")
        logger.warning(
            "[rst] unknown visit node: '%r - %r", node.__class__.__name__, node
        )

    def unknown_departure(self, node):
        classname = node.__class__.__name__
        if classname in {
            "JupyterKernelNode",
            "JupyterCellNode",
            "JupyterWidgetViewNode",
            "JupyterWidgetStateNode",
            "ThebeSourceNode",
            "ThebeOutputNode",
            "ThebeButtonNode",
        }:
            # due to jupyter_sphinx
            return
        logger = logging.getLogger("RstBuilder")
        logger.warning(
            "[rst] unknown depart node: %r - %r", node.__class__.__name__, node
        )


class _BodyPlaceholder:
    def __init__(self, builder):
        self.lines = []
        self.logger = logging.getLogger("RstBuilder")

    def append(self, element):
        if isinstance(element, str):
            el = element.replace("\n", " ")
            if len(el) > 50:
                el = el[:50] + "..."
            self.logger.warning("[rst] body.append was called with string %r", el)
        else:
            self.logger.warning(
                "[rst] body.append was called with type %", type(element)
            )
        self.lines.append(element)


class RstBuilder(Builder):
    """
    Defines a :epkg:`RST` builder.
    """

    name = "rst"
    format = "rst"
    file_suffix = ".rst"
    link_suffix = None  # defaults to file_suffix
    default_translator_class = RstTranslator

    def __init__(self, *args, **kwargs):
        """
        Constructor, add a logger.
        """
        Builder.__init__(self, *args, **kwargs)
        self.logger = logging.getLogger("RstBuilder")
        # Should not be populated, it may be due to a function
        # implemented for HTML but used for RST.
        self.body = _BodyPlaceholder(self)

    def init(self):
        """
        Load necessary templates and perform initialization.
        """
        if self.config.rst_file_suffix is not None:
            self.file_suffix = self.config.rst_file_suffix
        if self.config.rst_link_suffix is not None:
            self.link_suffix = self.config.rst_link_suffix
        if self.link_suffix is None:
            self.link_suffix = self.file_suffix

        # Function to convert the docname to a reST file name.
        def file_transform(docname):
            return docname + self.file_suffix

        # Function to convert the docname to a relative URI.
        def link_transform(docname):
            return docname + self.link_suffix

        if self.config.rst_file_transform is not None:
            self.file_transform = self.config.rst_file_transform
        else:
            self.file_transform = file_transform
        if self.config.rst_link_transform is not None:
            self.link_transform = self.config.rst_link_transform
        else:
            self.link_transform = link_transform
        self.rst_image_dest = self.config.rst_image_dest

    def get_outdated_docs(self):
        """
        Return an iterable of input files that are outdated.
        This method is taken from ``TextBuilder.get_outdated_docs()``
        with minor changes to support ``(confval, rst_file_transform))``.
        """
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            sourcename = os.path.join(self.env.srcdir, docname + self.file_suffix)
            targetname = os.path.join(self.outdir, self.file_transform(docname))

            try:
                targetmtime = os.path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = os.path.getmtime(sourcename)
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname, typ=None):
        return self.link_transform(docname)

    def prepare_writing(self, docnames):
        self.writer = RstWriter(self)

    def get_outfilename(self, pagename):
        """
        Overwrites *get_target_uri* to control file names.
        """
        return f"{self.outdir}/{pagename}.rst".replace("\\", "/")

    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding="utf-8")
        self.current_docname = docname
        self.writer.write(doctree, destination)
        ctx = None
        self.handle_page(docname, ctx, event_arg=doctree)

    def handle_page(
        self, pagename, addctx, templatename=None, outfilename=None, event_arg=None
    ):
        if templatename is not None:
            raise NotImplementedError("templatename must be None.")
        outfilename = self.get_outfilename(pagename)
        ensuredir(os.path.dirname(outfilename))
        with open(outfilename, "w", encoding="utf-8") as f:
            f.write(self.writer.output)

    def finish(self):
        pass


class RstWriter(writers.Writer):
    """
    Defines a :epkg:`RST` writer.
    """

    supported = ("text",)
    settings_spec = ("No options here.", "", ())
    settings_defaults = {}
    translator_class = RstTranslator

    output = None

    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder

    def translate(self):
        visitor = self.builder.create_translator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.body


def setup(app):
    """
    Initializes the :epkg:`RST` builder.
    """
    app.add_builder(RstBuilder)
    app.add_config_value("rst_file_suffix", ".rst", "env")
    app.add_config_value("rst_link_suffix", None, "env")
    app.add_config_value("rst_file_transform", None, "env")
    app.add_config_value("rst_link_transform", None, "env")
    app.add_config_value("rst_indent", STDINDENT, "env")
    app.add_config_value("rst_image_dest", None, "env")
