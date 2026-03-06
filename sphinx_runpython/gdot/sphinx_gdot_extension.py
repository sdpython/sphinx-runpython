import os
import logging
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from typing import Any
import sphinx
from sphinx.ext.graphviz import (
    latex_visit_graphviz,
    text_visit_graphviz,
    render_dot,
    GraphvizError,
    ClickableMapDefinition,
    __,
)
from ..ext_helper import get_env_state_info
from ..ext_io_helper import download_requirejs, get_url_content_timeout
from ..runpython.sphinx_runpython_extension import run_python_script


class gdot_node(nodes.admonition):
    """
    Defines ``gdot`` node.
    """

    pass


class GDotDirective(Directive):
    """
    A ``gdot`` node displays a :epkg:`DOT` graph.
    The build choose :epkg:`SVG` for :epkg:`HTML` format and image for
    other format unless it is specified.

    * *format*: SVG or HTML
    * *script*: boolean or a string to indicate than the standard output
        should only be considered after this substring
    * *url*: url to :epkg:`viz.js`, only if format *SVG* is selected
    * *process*: run the script in an another process

    Example::

        .. gdot::

            digraph foo {
                "bar" -> "baz";
            }

    Which gives:

    .. gdot::

        digraph foo {
            "bar" -> "baz";
        }

    The directive also accepts scripts producing
    dot graphs on the standard output. Option *script*
    must be specified. This extension loads
    `sphinx.ext.graphviz <https://www.sphinx-doc.org/
    en/master/usage/extensions/graphviz.html>`_
    if not added to the list of extensions:

    Example::

        .. gdot::
            :format: png

            digraph foo {
                "bar" -> "baz";
            }

    .. gdot::
        :format: png

        digraph foo {
            "bar" -> "baz";
        }

    The output can be produced by a script::

        .. gdot::
            :script:

            print('''
                digraph foo {
                    "bar" -> "baz";
                }
            ''')

    .. gdot::
        :script:

        print('''
            digraph foo {
                "bar" -> "baz";
            }
        ''')
    """

    node_class = gdot_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "format": directives.unchanged,
        "script": directives.unchanged,
        "url": directives.unchanged,
        "process": directives.unchanged,
    }

    _default_url = "https://cdnjs.cloudflare.com/ajax/libs/viz.js/1.8.0/viz-lite.js"

    def run(self):
        """Builds the collapse text."""
        # retrieves the parameters
        if "format" in self.options:  # noqa: SIM401
            format = self.options["format"]
        else:
            format = "svg"
        url = self.options.get("url", "local")
        bool_set_ = (True, 1, "True", "1", "true", "")
        process = "process" in self.options and self.options["process"] in bool_set_
        if url == "local":
            url = GDotDirective._default_url

        info = get_env_state_info(self)
        docname = info["docname"]
        if url == "local":
            if docname is None or "HERE" not in info:
                url = GDotDirective._default_url
                logger = logging.getLogger("gdot")
                logger.warning("[gdot] docname is none, falling back to %r.", url)
            else:
                spl = docname.split("/")
                sp = [".."] * (len(spl) - 1) + ["_static", "viz.js"]
                url = "/".join(sp)

        if "script" in self.options:
            script = self.options["script"]
            if script in (0, "0", "False", "false"):
                script = None
            elif script in (1, "1", "True", "true", ""):
                script = ""
            elif len(script) == 0:
                raise RuntimeError(
                    "script should be a string to indicate"
                    " the beginning of DOT graph."
                )
        else:
            script = False

        # executes script if any
        content = "\n".join(self.content)
        if script or script == "":
            stdout, stderr, _ = run_python_script(content, process=process)

            if stderr:
                out = [
                    "use_kernel_func_from_hub",
                    "is deprecated, use",
                    "was set in the config but",
                    "The axis name: batch will not be used",
                ]
                if isinstance(stderr, str):
                    stderr = "\n".join(
                        [_ for _ in stderr.split("\n") if all(o not in _ for o in out)]
                    )
                else:
                    bout = [_.encode("utf-8") for _ in out]
                    stderr = b"\n".join(
                        [
                            _
                            for _ in stderr.split(b"\n")
                            if all(o not in _ for o in bout)
                        ]
                    )

            if stderr:
                logger = logging.getLogger("gdot")
                logger.warning("[gdot] a dot graph cannot be draw due to %s", stderr)
            content = stdout
            if script:
                spl = content.split(script)
                if len(spl) > 2:
                    logger = logging.getLogger("gdot")
                    logger.warning("[gdot] too many output lines %s", content)
                content = spl[-1]

        node = gdot_node(
            format=format,
            code=content,
            url=url,
            options={"docname": docname},
            use_sphinx_graphviz=True,
        )
        return [node]


def visit_gdot_node_rst(self, node):
    """visit collapse_node"""
    self.new_state(0)
    self.add_text(".. gdot::" + self.nl)
    if node["format"] != "?":
        self.add_text("    :format: " + node["format"] + self.nl)
    if node["url"]:
        self.add_text("    :url: " + node["url"] + self.nl)
    self.new_state(self.indent)
    for row in node["code"].split("\n"):
        self.add_text(row + self.nl)


def depart_gdot_node_rst(self, node):
    """depart collapse_node"""
    self.end_state()
    self.end_state(wrap=False)


_DUMMY_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
    '<text x="10" y="50">DISABLED FOR TESTS</text>'
    "</svg>"
)

_DUMMY_PNG_HTML = (
    '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQ'
    'AABjkB6QAAAABJRU5ErkJggg==" alt="DISABLED FOR TESTS" />'
)


def _emit_dummy_output(self, format: str = "svg"):
    """Emit a placeholder graphic when ``UNITTEST_GOING=1`` is set."""
    self.body.append('<div class="graphviz">')
    if format == "png":
        self.body.append(_DUMMY_PNG_HTML)
    else:
        self.body.append(_DUMMY_SVG)
    self.body.append("</div>\n")
    raise nodes.SkipNode


def render_dot_html(
    self,
    node: gdot_node,
    code: str,
    options: dict[str, Any],
    prefix: str = "gdot",
    imgcls: str | None = None,
    alt: str | None = None,
    filename: str | None = None,
    format: str = "svg",
) -> tuple[str, str]:
    if os.environ.get("UNITTEST_GOING", "0") == "1":
        _emit_dummy_output(self, format=format)

    if format not in {"png", "svg"}:
        logger = logging.getLogger(__name__)
        logger.warning(__("format must be either 'png' or 'svg', but is %r"), format)
    try:
        fname, outfn = render_dot(self, code, options, format, prefix, filename)
    except GraphvizError as exc:
        logger.warning(__("dot code %r: %s"), code, exc)
        raise nodes.SkipNode from exc

    classes = [imgcls, "graphviz", *node.get("classes", [])]
    imgcls = " ".join(filter(None, classes))

    if fname is None:
        self.body.append(self.encode(code))
    else:
        src = fname.as_posix()
        if alt is None:
            alt = node.get("alt", self.encode(code).strip())
        if "align" in node:
            align = node["align"]
            self.body.append(f'<div align="{align}" class="align-{align}">')
        if format == "svg":
            self.body.append('<div class="graphviz">')
            self.body.append(
                f'<object data="{src}" type="image/svg+xml" class="{imgcls}">\n'
            )
            self.body.append(f'<p class="warning">{alt}</p>')
            self.body.append("</object></div>\n")
        else:
            assert outfn is not None
            with open(f"{outfn}.map", encoding="utf-8") as mapfile:
                map_content = mapfile.read()
            imgmap = ClickableMapDefinition(f"{outfn}.map", map_content, dot=code)
            if imgmap.clickable:
                # has a map
                self.body.append('<div class="graphviz">')
                self.body.append(
                    f'<img src="{src}" alt="{alt}" usemap="#{imgmap.id}" class="{imgcls}" />'
                )
                self.body.append("</div>\n")
                self.body.append(imgmap.generate_clickable_map())
            else:
                # nothing in image map
                self.body.append('<div class="graphviz">')
                self.body.append(f'<img src="{src}" alt="{alt}" class="{imgcls}" />')
                self.body.append("</div>\n")
        if "align" in node:
            self.body.append("</div>\n")

    raise nodes.SkipNode


def visit_gdot_node_html_svg(self, node):
    """visit collapse_node"""
    if node["use_sphinx_graphviz"]:
        render_dot_html(
            self, node, node["code"], node["options"], filename=node.get("filename")
        )
        return

    def process(text):
        text = text.replace("\\", "\\\\")
        text = text.replace("\n", "\\n")
        text = text.replace('"', '\\"')
        return text

    nid = str(id(node))

    content = """
    <div id="gdot-{0}-cont"><div id="gdot-{0}" style="width:100%;height:100%;"></div>
    """.format(nid)

    script = (
        """
    require(['__URL__'], function() { var svgGraph = Viz("__DOT__");
    document.getElementById('gdot-__ID__').innerHTML = svgGraph; });
    """.replace("__ID__", nid)
        .replace("__DOT__", process(node["code"]))
        .replace("__URL__", node["url"])
    )

    # find the path
    source = self.document.attributes["source"]
    folder = os.path.dirname(source)
    # from_ = self.builder.get_target_uri(source)
    # req = self.builder.get_target_uri("_static/require.js")
    # rel = self.builder.get_relative_uri(from_, req)

    if os.path.exists(folder):
        while not os.path.exists(os.path.join(folder, "conf.py")):
            cts = set(os.listdir(folder))
            if "conf.py" in cts:
                break
            exts = {os.path.splitext(name)[-1] for name in cts}
            if ".rst" not in exts:
                folder = None
                break
            folder = os.path.split(folder)[0]
    else:
        folder = None

    self.body.append(content)
    if folder is None:
        self.body.append(
            '<script src="_static/require.js"></script><script>'
            "{0}{1}{0}</script>{0}".format("\n", script)
        )
    else:
        current = os.path.dirname(source)
        rel = os.path.relpath(current, folder)
        if rel not in {"", "."}:
            rel = rel.replace("\\", "/")
            rel = f"{'/'.join(['..'] * len(rel.split('/')))}/"
        else:
            rel = ""
        self.body.append(
            '<script src="{2}_static/require.js"></script><script>'
            "{0}{1}{0}</script>{0}".format("\n", script, rel)
        )


def depart_gdot_node_html_svg(self, node):
    """
    depart collapse_node
    """
    self.body.append("</div>")


def visit_gdot_node_html(self, node):
    """
    visit collapse_node, the function switches between
    `graphviz.py <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/graphviz.py>`_
    and the :epkg:`SVG` format.
    """
    if node["format"].lower() == "png":
        if os.environ.get("UNITTEST_GOING", "0") == "1":
            _emit_dummy_output(self, format="png")
        from sphinx.ext.graphviz import html_visit_graphviz

        return html_visit_graphviz(self, node)
    if node["format"].lower() in ("?", "svg"):
        return visit_gdot_node_html_svg(self, node)
    raise RuntimeError(f"Unexpected format for graphviz '{node['format']}'.")


def depart_gdot_node_html(self, node):
    """
    depart collapse_node
    """
    if node["format"] == "png":
        return None
    return depart_gdot_node_html_svg(self, node)


def copy_js_files(app):
    logger = logging.getLogger("gdot")
    dest = app.config.html_static_path
    if isinstance(dest, list) and len(dest) > 0:
        dest = dest[0]
    else:
        logger.warning(
            "[gdot] unable to locate 'html_static_path' (%r), "
            "unable to use local viz.js.",
            app.config.html_static_path,
        )
        return

    srcdir = app.builder.srcdir
    if not os.path.exists(srcdir):
        raise FileNotFoundError(f"Source file is wrong {srcdir!r}.")
    destf = os.path.join(os.path.abspath(srcdir), dest)
    if not os.path.exists(destf):
        logger.warning(
            "[gdot] destination folder %r does not exists, "
            "unable to use local viz.js.",
            destf,
        )
        return

    # viz.js
    file_dest = os.path.join(destf, "viz.js")
    if not os.path.exists(file_dest):
        logger.info("[gdot] viz.js, use %r", GDotDirective._default_url)

        try:
            content = get_url_content_timeout(
                GDotDirective._default_url, output=file_dest, raise_exception=False
            )
        except Exception as e:
            logger.warning("[gdot] download failed due to %r", e)
            content = None

        if content is None:
            logger.warning(
                "[gdot] unable to download %r to %r",
                GDotDirective._default_url,
                file_dest,
            )
        else:
            logger.info(
                "[gdot] download %r to %r", GDotDirective._default_url, file_dest
            )

    # require.js
    file_dest = os.path.join(destf, "require.js")
    if not os.path.exists(file_dest):
        logger.info("[gdot] download %r", file_dest)
        try:
            download_requirejs(destf)
        except Exception as e:
            logger.warning("[gdot] download_requirejs failed due to %r", e)

    if not os.path.exists(file_dest):
        # It adds <script async="defer" src="_static/require.js"></script>
        # at the bottom of the file. It needs to be at the beginning.
        # app.add_js_file("require.js", priority=200)
        logger.warning("[gdot] %r not installed.", file_dest)


def setup(app):
    """
    setup for ``gdot`` (sphinx)
    """
    if "sphinx.ext.graphviz" not in app.config.extensions:
        from sphinx.ext.graphviz import setup as setup_g  # pylint: disable=W0611

        setup_g(app)

    app.connect("builder-inited", copy_js_files)

    app.add_node(
        gdot_node,
        html=(visit_gdot_node_html, depart_gdot_node_html),
        epub=(visit_gdot_node_html, depart_gdot_node_html),
        elatex=(latex_visit_graphviz, None),
        latex=(latex_visit_graphviz, None),
        text=(text_visit_graphviz, None),
        md=(text_visit_graphviz, None),
        rst=(visit_gdot_node_rst, depart_gdot_node_rst),
    )

    app.add_directive("gdot", GDotDirective)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
