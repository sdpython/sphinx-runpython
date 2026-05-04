import hashlib
import logging
from docutils import nodes
from docutils.parsers.rst import directives, Directive
import sphinx
from ..ext_helper import get_env_state_info
from ..runpython.sphinx_runpython_extension import run_python_script

logger = logging.getLogger("mermaidjs")

#: Default CDN URL for the mermaid JavaScript library.
_MERMAID_JS_URL = "https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"


class mermaidjs_node(nodes.General, nodes.Element):
    """
    Defines ``mermaidjs`` node.
    """

    pass


class MermaidDirective(Directive):
    """
    A ``mermaidjs`` node displays a `Mermaid <https://mermaid.js.org/>`_ diagram.

    For *HTML* output the diagram is rendered client-side by embedding the
    Mermaid JavaScript library (loaded from a CDN or a local copy).
    For *LaTeX* / *text* / *RST* output the raw Mermaid source is included.

    Supported options:

    * *script*: boolean or a string that marks the beginning of the Mermaid
      source in the standard output of the embedded Python script.  When this
      option is present the directive body is interpreted as Python code whose
      ``stdout`` contains the diagram definition.
    * *process*: run the Python script in a separate process.

    Example – inline diagram::

        .. mermaidjs::

            graph LR
                A --> B --> C

    Which gives:

    .. mermaidjs::

        graph LR
            A --> B --> C

    Example – script-generated diagram::

        .. mermaidjs::
            :script:

            print(\"\"\"
            graph LR
                A --> B
            \"\"\")

    .. mermaidjs::
        :script:

        print(\"\"\"
        graph LR
            A --> B
        \"\"\")
    """

    node_class = mermaidjs_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "script": directives.unchanged,
        "process": directives.unchanged,
    }

    def run(self):
        """Build the mermaidjs node."""
        bool_set_ = (True, 1, "True", "1", "true", "")
        process = "process" in self.options and self.options["process"] in bool_set_

        info = get_env_state_info(self)
        docname = info["docname"]

        if "script" in self.options:
            script = self.options["script"]
            if script in (0, "0", "False", "false"):
                script = None
            elif script in (1, "1", "True", "true", ""):
                script = ""
            # else: keep script as-is to use it as a split token
        else:
            script = False

        # Execute the script and use its stdout as diagram source, if requested.
        content = "\n".join(self.content)
        if script or script == "":
            env = info.get("env")
            doc_prefix = docname.split("/")[-1] if docname else ""
            cache_key = (
                f"{doc_prefix}:"
                + hashlib.sha256(f"{content}:{process}".encode()).hexdigest()
            )
            if env is not None:
                if not hasattr(env, "mermaidjs_script_cache"):
                    env.mermaidjs_script_cache = {}
                cached = env.mermaidjs_script_cache.get(cache_key, None)
            else:
                cached = None

            if cached is not None:
                stdout, stderr = cached
            else:
                stdout, stderr, _ = run_python_script(content, process=process)
                if env is not None:
                    env.mermaidjs_script_cache[cache_key] = (stdout, stderr)

            if stderr:
                logger.warning(
                    "[mermaidjs] a diagram cannot be drawn due to %s", stderr
                )
            content = stdout
            if script:
                spl = content.split(script)
                if len(spl) > 2:
                    logger.warning("[mermaidjs] too many output lines %s", content)
                content = spl[-1]

        node = mermaidjs_node(code=content, options={"docname": docname})
        return [node]


# ---------------------------------------------------------------------------
# Visitor helpers
# ---------------------------------------------------------------------------


def visit_mermaidjs_node_html(self, node):
    """Render the mermaidjs node in HTML output."""
    code = node["code"].strip()
    # Emit a <pre class="mermaid"> block; mermaid.js will replace it at runtime.
    self.body.append(
        f'<div class="mermaid-diagram">'
        f'<pre class="mermaid">{self.encode(code)}</pre>'
        f"</div>\n"
    )
    raise nodes.SkipNode


def depart_mermaidjs_node_html(self, node):
    """Depart the mermaidjs HTML node. Not called because the visitor raises SkipNode."""


def visit_mermaidjs_node_rst(self, node):
    """Render the mermaidjs node in RST output."""
    self.new_state(0)
    self.add_text(".. mermaidjs::" + self.nl)
    self.new_state(self.indent)
    for row in node["code"].split("\n"):
        self.add_text(row + self.nl)


def depart_mermaidjs_node_rst(self, node):
    """Depart mermaidjs node in RST output."""
    self.end_state()
    self.end_state(wrap=False)


def visit_mermaidjs_node_text(self, node):
    """Render the mermaidjs node in plain-text output."""
    self.new_state(0)
    self.add_text("[mermaidjs diagram]\n")
    self.new_state(self.indent)
    for row in node["code"].split("\n"):
        self.add_text(row + self.nl)


def depart_mermaidjs_node_text(self, node):
    """Depart mermaidjs node in text output."""
    self.end_state()
    self.end_state(wrap=False)


def visit_mermaidjs_node_latex(self, node):
    """Render the mermaidjs node in LaTeX output (verbatim source)."""
    code = node["code"].strip()
    self.body.append("\n\\begin{verbatim}\n")
    self.body.append(code)
    self.body.append("\n\\end{verbatim}\n")
    raise nodes.SkipNode


def depart_mermaidjs_node_latex(self, node):
    """Depart the mermaidjs LaTeX node. Not called because the visitor raises SkipNode."""


# ---------------------------------------------------------------------------
# JS injection
# ---------------------------------------------------------------------------


def add_mermaid_js(app):
    """Inject the Mermaid JS library into HTML pages."""
    if app.builder.format != "html":
        return
    app.add_js_file(_MERMAID_JS_URL, **{"loading_method": "async"})
    # Initialise mermaid after the DOM is ready.
    app.add_js_file(
        None,
        body="document.addEventListener('DOMContentLoaded', function() { mermaid.initialize({startOnLoad: true}); });",
    )


# ---------------------------------------------------------------------------
# Extension setup
# ---------------------------------------------------------------------------


def setup(app):
    """
    setup for ``mermaidjs`` (sphinx)
    """
    app.connect("builder-inited", add_mermaid_js)

    app.add_node(
        mermaidjs_node,
        html=(visit_mermaidjs_node_html, depart_mermaidjs_node_html),
        epub=(visit_mermaidjs_node_html, depart_mermaidjs_node_html),
        latex=(visit_mermaidjs_node_latex, depart_mermaidjs_node_latex),
        text=(visit_mermaidjs_node_text, depart_mermaidjs_node_text),
        rst=(visit_mermaidjs_node_rst, depart_mermaidjs_node_rst),
        md=(visit_mermaidjs_node_text, depart_mermaidjs_node_text),
    )

    app.add_directive("mermaidjs", MermaidDirective)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
