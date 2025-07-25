import sys
import os
from contextlib import redirect_stdout, redirect_stderr
import traceback
import warnings
from io import StringIO
import sphinx
from docutils import nodes, core
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util import logging
from ..language import TITLES
from .run_cmd import run_cmd
from ..collapse.sphinx_collapse_extension import collapse_node


def remove_extra_spaces_and_black(
    filename: str, apply_black=True, is_string=None
) -> str:
    """
    Removes extra spaces in a filename, replaces the file in place.

    :param filename: file name or string (but it assumes it is python).
    :param apply_black: if True, calls :epkg:`black` on the file
    :param is_string: force *filename* to be a string
    :return: number of removed extra spaces
    """
    encoding = None
    initial_content = None
    if "\n" in filename or (is_string is not None and is_string):
        ext = ".py"
        lines = filename.replace("\r", "").split("\n")
        filename = None
    else:
        ext = os.path.splitext(filename)[-1]
        if ext in (".bat", ".py", ".sh", ".pyx", ".pxd"):
            try:
                with open(filename, "r") as f:
                    lines = f.readlines()
                encoding = None
            except PermissionError as e:
                raise PermissionError(filename) from e
            except UnicodeDecodeError as e:
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    encoding = "utf-8"
                except Exception:
                    raise RuntimeError(
                        f"unable to load file {filename} due to unicode errors"
                    ) from e
            initial_content = "".join(lines)
        else:
            try:
                with open(filename, "r", encoding="utf-8-sig") as f:
                    lines = f.readlines()
                encoding = "utf-8"
            except PermissionError as e:
                raise PermissionError(filename) from e
            except UnicodeDecodeError as e:
                try:
                    with open(filename, "r") as f:
                        lines = f.readlines()
                    encoding = None
                except Exception:
                    raise RuntimeError(
                        f"unable to load file {filename} due to unicode errors"
                    ) from e
            initial_content = "".join(lines)

    if (
        filename is not None
        and len(lines) == 0
        and not filename.endswith("__init__.py")
    ):
        raise ValueError(f"File '{filename}' is empty, encoding='{encoding}'.")

    if filename is not None and ext in (".py", ".pyx", ".pxd"):
        if (
            encoding is not None
            and len(lines) > 0
            and "#-*-coding:utf-8-*-" in lines[0].replace(" ", "")
        ):
            with open(filename, "r", encoding="utf8") as f:
                try:
                    lines = f.readlines()
                except UnicodeDecodeError as e:
                    raise RuntimeError("unable to read: " + filename) from e
            encoding = "utf8"
        else:
            encoding = None

    def cdiff(lines):
        lines2 = [_.rstrip(" \r\n") for _ in lines]
        last = len(lines2) - 1
        while last >= 0 and len(lines2[last]) == 0:
            last -= 1
        last += 1
        lines2 = lines2[:last]

        diff = len("".join(lines)) - len("\n".join(lines2)) + len(lines)
        return diff, lines2

    diff, lines2 = cdiff(lines)

    if filename is not None:
        ext = os.path.splitext(filename)[-1]
    if ext in (".py",) and apply_black:
        # delayed import to speed up import of pycode
        from black import format_str, FileMode

        r = format_str("\n".join(lines2), mode=FileMode())

        if len(lines) > 0 and (len(lines2) == 0 or len(lines2) < len(lines) // 2):
            raise ValueError(
                "Resulting file is empty for '{3}',"  # noqa: UP030
                "\ninitial number of lines "
                "{0} encoding='{1}' diff={2}".format(
                    len(lines), encoding, diff, filename
                )
            )
        if filename is None:
            return r
        elif r != initial_content:
            if encoding is None:
                with open(filename, "w") as f:
                    f.write(r)
            else:
                with open(filename, "w", encoding="utf8") as f:
                    f.write(r)
        if r != "".join(lines):
            diff, lines2 = cdiff(r.split("\n"))
        else:
            diff = 0
    elif ext in (".rst", ".md", ".pyx", ".pxd"):
        lines2 = [_.replace("\r", "").rstrip("\n ") for _ in lines]
        rem = set()
        for i, line in enumerate(lines2):
            if i >= 1 and line == lines2[i - 1] == "":
                rem.add(i)
        lines2 = [_ for i, _ in enumerate(lines2) if i not in rem]
        if len(lines) > 0 and len(lines2[-1]) > 0:
            lines2.append("")
        if len(lines) > 0 and len(lines2) == 0:
            raise ValueError(
                f"Resulting file is empty for {filename!r},"
                f"\ninitial number of lines {len(lines)} encoding={encoding!r} "
                f"len(rem)={len(rem)} diff={diff}\nBeginning:"
                f"\n{''.join(lines[:5 if len(lines) > 5 else len(lines)])}"
            )
        if len(lines2) < len(lines) // 2:
            lines2_ = [_ for _ in lines2 if _ and _ != "\n"]
            lines_ = [_ for _ in lines if _ and _ != "\n"]
            if len(lines2_) < len(lines_) // 2:
                raise ValueError(
                    f"Resulting file is almost empty for {filename!r},"
                    f"\ninitial number of lines {len(lines_)} encoding={encoding!r} "
                    f"len(rem)={len(rem)} diff={diff}\nBeginning:"
                    f"\n{''.join(lines_[:5 if len(lines_) > 5 else len(lines_)])}"
                )
        rl = "".join(lines)
        r2 = "\n".join(lines2)
        if r2 != rl:
            if encoding is None:
                with open(filename, "w") as f:
                    f.write("\n".join(lines2))
            else:
                with open(filename, "w", encoding="utf8") as f:
                    f.write("\n".join(lines2))
            diff = max(1, diff)
        else:
            diff = 0
    elif diff != 0:
        if len(lines) > 0 and (len(lines2) == 0 or len(lines2) < len(lines) // 2):
            raise ValueError(
                f"Resulting file is empty for '{filename}",
                f"\ninitial number of lines {len(lines)} "
                f"encoding='{encoding}' diff={diff}",
            )
        r1 = "".join(lines)
        r2 = "\n".join(lines2)
        if r2 != r1:
            if encoding is None:
                with open(filename, "w") as f:
                    f.write("\n".join(lines2))
            else:
                with open(filename, "w", encoding="utf8") as f:
                    f.write("\n".join(lines2))

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Issue when applying black with filename: '{filename}'."
        )
    return diff


class RunPythonCompileError(Exception):
    """
    Exception raised when a piece of code
    included in the documentation does not compile
    """

    pass


class RunPythonExecutionError(Exception):
    """
    Exception raised when a piece of code
    included in the documentation raises an exception.
    """

    pass


def run_python_script(
    script,
    params=None,
    comment=None,
    setsysvar=None,
    process=False,
    exception=False,
    warningout=None,
    chdir=None,
    context=None,
    store_in_file=None,
):
    """
    Executes a script :epkg:`python` as a string.

    :param script: python script
    :param params: params to add before the execution
    :param comment: message to add in a exception when the script fails
    :param setsysvar: if not None, add a member to module *sys*,
        set up this variable to True,
        if is remove after the execution
    :param process: run the script in a separate process
    :param exception: expects an exception to be raised,
        fails if it is not, the function returns no output and the
        error message
    :param warningout: warning to disable (name of warnings)
    :param chdir: change directory before running this script (if not None)
    :param context: if not None, added to the local context
    :param store_in_file: stores the script into this file
        and calls tells python the source can be found here,
        that is useful is the script is using module
        ``inspect`` to retrieve the source which are not
        stored in memory
    :return: stdout, stderr, context

    If the execution throws an exception such as
    ``NameError: name 'math' is not defined`` after importing
    the module ``math``. It comes from the fact
    the domain name used by the function
    `exec <https://docs.python.org/3/library/functions.html#exec>`_
    contains the declared objects. Example:

    ::

        import math
        def coordonnees_polaires(x,y):
            rho = math.sqrt(x*x+y*y)
            theta = math.atan2 (y,x)
            return rho, theta
        coordonnees_polaires(1, 1)

    The code can be modified into:

    ::

        def fake_function():
            import math
            def coordonnees_polaires(x,y):
                rho = math.sqrt(x*x+y*y)
                theta = math.atan2 (y,x)
                return rho, theta
            coordonnees_polaires(1, 1)
        fake_function()

    Section :ref:`l-image-rst-runpython` explains
    how to display an image with this directive.
    """

    def warning_filter(warningout):
        if warningout in (None, ""):
            warnings.simplefilter("always")
        elif isinstance(warningout, str):
            li = [_.strip() for _ in warningout.split()]
            warning_filter(li)
        elif isinstance(warningout, list):

            def interpret(s):
                return eval(s) if isinstance(s, str) else s

            warns = [interpret(w) for w in warningout]
            for w in warns:
                warnings.simplefilter("ignore", w)
        else:
            raise ValueError(f"Unexpected value for warningout: {warningout}")

    if params is None:
        params = {}

    if process:
        if context is not None and len(context) != 0:
            raise RunPythonExecutionError(
                "context cannot be used if the script runs in a separate process."
            )

        cmd = sys.executable
        header = ["# coding: utf-8", "import sys"]
        if setsysvar:
            header.append(f"sys.{setsysvar} = True")
        add = 0
        for path in sys.path:
            if path.endswith(("source", "source/", "source\\")):
                header.append(
                    "sys.path.append('{}')".format(path.replace("\\", "\\\\"))
                )
                add += 1
        if add == 0:
            for path in sys.path:
                if path.endswith(("src", "src/", "src\\")):
                    header.append(
                        "sys.path.append('{}')".format(path.replace("\\", "\\\\"))
                    )
                    add += 1
        if add == 0:
            # It did not find any path linked to the copy of
            # the current module in the documentation
            # it assumes the first path of `sys.path` is part
            # of the unit test.
            path = sys.path[0]
            path = os.path.join(path, "..", "..", "src")
            if os.path.exists(path):
                header.append(
                    "sys.path.append('{}')".format(
                        path.replace("\\", "\\\\")
                    )  # noqa: UP030
                )
                add += 1
            else:
                path = sys.path[0]
                path = os.path.join(path, "src")
                if os.path.exists(path):
                    header.append(
                        "sys.path.append('{}')".format(
                            path.replace("\\", "\\\\")
                        )  # noqa: UP030
                    )
                    add += 1

        if add == 0:
            # We do nothing unless the execution failed.
            exc_path = RunPythonExecutionError(
                "Unable to find a path to add:\n{}".format(
                    "\n".join(sys.path)
                )  # noqa: UP030
            )
        else:
            exc_path = None
        header.append("")
        script = "\n".join(header) + script

        if store_in_file is not None:
            with open(store_in_file, "w", encoding="utf-8") as f:
                f.write(script)
            script_arg = None
            cmd += " " + store_in_file
        else:
            script_arg = script

        try:
            out, err = run_cmd(cmd, script_arg, wait=True, change_path=chdir)
            return out, err, None
        except Exception as ee:
            if not exception:
                message = (  # noqa: UP030
                    "--SCRIPT--\n{0}\n--PARAMS--\n{1}\n--COMMENT--\n"
                    "{2}\n--ERR--\n{3}\n--OUT--\n{4}\n--EXC--\n{5}"
                    ""
                ).format(script, params, comment, "", str(ee), ee)
                if exc_path:
                    message += f"\n---EXC--\n{exc_path}"
                raise RunPythonExecutionError(message) from ee
            return str(ee), str(ee), None
    else:
        if store_in_file:
            raise NotImplementedError(
                "store_in_file is only implemented if process is True."
            )
        try:
            obj = compile(script, "", "exec")
        except Exception as ec:
            if comment is None:
                comment = ""
            if not exception:
                message = f"SCRIPT:\n{script}\nPARAMS\n{params}\nCOMMENT\n{comment}"
                raise RunPythonCompileError(message) from ec
            return "", f"Cannot compile the do to {ec}", None

        globs = globals().copy()
        loc = locals()
        for k, v in params.items():
            loc[k] = v
        loc["__dict__"] = params
        if context is not None:
            for k, v in context.items():
                globs["__runpython__" + k] = v
        globs["__runpython__script__"] = script

        if setsysvar is not None:
            sys.__dict__[setsysvar] = True

        sout = StringIO()
        serr = StringIO()
        with redirect_stdout(sout), redirect_stderr(sout), warnings.catch_warnings():
            warning_filter(warningout)

            if chdir is not None:
                current = os.getcwd()
                os.chdir(chdir)

            try:
                exec(obj, globs, loc)
            except Exception as ee:
                if chdir is not None:
                    os.chdir(current)
                if setsysvar is not None:
                    del sys.__dict__[setsysvar]
                if comment is None:
                    comment = ""
                gout = sout.getvalue()
                gerr = serr.getvalue()

                excs = traceback.format_exc()
                lines = excs.split("\n")
                excs = "\n".join(
                    _ for _ in lines if "sphinx_runpython_extension.py" not in _
                )

                if not exception:
                    message = (  # noqa: UP030
                        "--SCRIPT--\n{0}\n--PARAMS--\n{1}\n--COMMENT--"
                        "\n{2}\n--ERR--\n{3}\n--OUT--\n{4}\n--EXC--"
                        "\n{5}\n--TRACEBACK--\n{6}"
                    ).format(script, params, comment, gout, gerr, ee, excs)
                    raise RunPythonExecutionError(message) from ee
                return (gout + "\n" + gerr), (gerr + "\n" + excs), None

            if chdir is not None:
                os.chdir(current)

        if setsysvar is not None:
            del sys.__dict__[setsysvar]

        gout = sout.getvalue()
        gerr = serr.getvalue()
        avoid = {"__runpython____WD__", "__runpython____k__", "__runpython____w__"}
        context = {
            k[13:]: v
            for k, v in globs.items()
            if k.startswith("__runpython__") and k not in avoid
        }
        return gout, gerr, context


class runpython_node(nodes.Structural, nodes.Element):
    """
    Defines *runpython* node.
    """

    pass


class RunPythonDirective(Directive):
    """
    Extracts script to run described by ``.. runpython::``
    and modifies the documentation.

    The following code prints the version of Python
    on the standard output. It is added to the documentation::

        .. runpython::
            :showcode:

            import sys
            print("sys.version_info=", str(sys.version_info))

    If give the following results:

    .. runpython::

        import sys
        print("sys.version_info=", str(sys.version_info))

    Options *showcode* can be used to display the code.
    The option *rst* will assume the output is in RST format and must be
    interpreted. *showout* will complement the RST output with the raw format.

    The directive has a couple of options:

    * ``:assert:`` condition to validate at the end of the execution
      to check it went right
    * ``:current:`` runs the script in the source file directory
    * ``:exception:`` the code throws an exception but it is expected.
      The error is displayed.
    * ``:indent:<int>`` to indent the output
    * ``:language:``: changes ``::`` into ``.. code-block:: language``
    * ``:linenos:`` to show line numbers
    * ``:noblack:`` if present, leaves the code as it is and does
      not apply black by default,
    * ``:numpy_precision: <precision>``, run ``numpy.set_printoptions(precision=...)``,
      precision is 3 by default
    * ``:process:`` run the script in an another process
    * ``:restore:`` restore the local context stored in :epkg:`sphinx` application
      by the previous call to *runpython*
    * ``:rst:`` to interpret the output, otherwise, it is considered as raw text
    * ``:setsysvar:`` adds a member to *sys* module,
      the module can act differently based on that information,
      if the value is left empty, *sys.enable_disabled_documented_pieces_of_code*
      will be be set up to *True*.
    * ``:showcode:`` to show the code before its output
    * ``:showout`` if *:rst:* is set up, this flag adds the raw rst
      output to check what is happening
    * ``:sin:<text_for_in>`` which text to display before the code (by default *In*)
    * ``:sout:<text_for_in>`` which text to display before the output (by default *Out*)
    * ``:sphinx:`` by default, function :epkg:`nested_parse_with_titles` is
      used to parse the output of the script, if this option is set to false,
      `publish-doctree
      <https://docutils.sourceforge.io/docs/api/publisher.html#publish-doctree>`_.
    * ``:store:`` stores the local context in :epkg:`sphinx`
      application to restore it later by another call to *runpython*
    * ``:toggle:`` add a button to hide or show the code, it takes the values
      ``code`` or ``out`` or ``both``. The direction then hides the given section
      but adds a button to show it.
    * ``:warningout:`` name of warnings to disable (ex: ``ImportWarning``),
      separated by spaces
    * ``:store_in_file:`` the directive store the script in a file,
        then executes this file (only if ``:process:`` is enabled),
        this trick is needed when the script to executes relies on
        function such :epkg:`*py:inspect:getsource` which requires
        the script to be stored somewhere in order to retrieve it.
    * ``:debug:`` if ``:rst:`` is used, it shows some information to help
      debugging.

    Option *rst* can be used the following way::

        .. runpython::
            :rst:

            for l in range(0,10):
                print("**line**", "*" +str(l)+"*")
                print('')

    Which displays interpreted :epkg:`RST`:

    .. runpython::
        :rst:

        for l in range(0,10):
            print("**line**", "*" +str(l)+"*")
            print('')

    If the directive produces RST text to be included later in the documentation,
    it is able to interpret
    `docutils directives <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_
    and `Sphinx directives
    <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_
    with function :epkg:`nested_parse_with_titles`. However, if this text contains
    titles, it is better to use option ``:sphinx: false``.
    Unless *process* option is enabled, global variables cannot be used.
    `sphinx-autorun <https://pypi.org/project/sphinx-autorun/>`_ offers a similar
    service except it cannot produce compile :epkg:`RST` content,
    hide the source and a couple of other options.
    Option *toggle* can hide or unhide the piece of code
    or/and its output.
    The directive also adds local variables such as
    ``__WD__`` which contains the path to the documentation
    which contains the directive. It is useful to load additional
    files ``os.path.join(__WD__, ...)``.

    .. runpython::
        :toggle: out
        :showcode:

        print("Hide or unhide this output.")
    """

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "indent": directives.unchanged,
        "showcode": directives.unchanged,
        "showout": directives.unchanged,
        "rst": directives.unchanged,
        "sin": directives.unchanged,
        "sout": directives.unchanged,
        "sphinx": directives.unchanged,
        "sout2": directives.unchanged,
        "setsysvar": directives.unchanged,
        "process": directives.unchanged,
        "exception": directives.unchanged,
        "noblack": directives.unchanged,
        "warningout": directives.unchanged,
        "toggle": directives.unchanged,
        "current": directives.unchanged,
        "assert": directives.unchanged,
        "language": directives.unchanged,
        "store": directives.unchanged,
        "restore": directives.unchanged,
        "numpy_precision": directives.unchanged,
        "store_in_file": directives.unchanged,
        "linenos": directives.unchanged,
        "debug": directives.unchanged,
    }
    has_content = True
    runpython_class = runpython_node

    def run(self):
        """
        Extracts the information in a dictionary,
        runs the script.

        :return: a list of nodes
        """
        # settings
        sett = self.state.document.settings
        language_code = sett.language_code
        lineno = self.lineno

        # add the instance to the global settings
        if hasattr(sett, "out_runpythonlist"):
            sett.out_runpythonlist.append(self)

        # env
        if hasattr(self.state.document.settings, "env"):
            env = self.state.document.settings.env
        else:
            env = None

        if env is None:
            docname = "___unknown_docname___"
        else:
            docname = env.docname

        # post
        bool_set = (True, 1, "True", "1", "true")
        bool_set_ = (True, 1, "True", "1", "true", "")
        p = {
            "showcode": "showcode" in self.options,
            "linenos": "linenos" in self.options,
            "showout": "showout" in self.options,
            "rst": "rst" in self.options,
            "debug": "debug" in self.options,
            "sin": self.options.get("sin", TITLES[language_code]["In"]),
            "sout": self.options.get("sout", TITLES[language_code]["Out"]),
            "sout2": self.options.get("sout2", TITLES[language_code]["Out2"]),
            "sphinx": "sphinx" not in self.options
            or self.options["sphinx"] in bool_set,
            "setsysvar": self.options.get("setsysvar", None),
            "process": "process" in self.options
            and self.options["process"] in bool_set_,
            "exception": "exception" in self.options
            and self.options["exception"] in bool_set_,
            "noblack": "noblack" in self.options
            and self.options["noblack"] in bool_set_,
            "warningout": self.options.get("warningout", "").strip(),
            "toggle": self.options.get("toggle", "").strip(),
            "current": "current" in self.options
            and self.options["current"] in bool_set_,
            "assert": self.options.get("assert", "").strip(),
            "language": self.options.get("language", "").strip(),
            "store_in_file": self.options.get("store_in_file", None),
            "numpy_precision": self.options.get("numpy_precision", "3").strip(),
            "store": "store" in self.options and self.options["store"] in bool_set_,
            "restore": "restore" in self.options
            and self.options["restore"] in bool_set_,
        }

        if p["setsysvar"] is not None and len(p["setsysvar"]) == 0:
            p["setsysvar"] = "enable_disabled_documented_pieces_of_code"
        dind = 0 if p["rst"] else 4
        p["indent"] = int(self.options.get("indent", dind))

        # run the script
        name = f"run_python_script_{id(p)}"
        if p["process"]:
            content = ["if True:"]
        else:
            content = [f"def {name}():"]

        if "numpy" in "\n".join(self.content) and p["numpy_precision"] not in (
            None,
            "None",
            "-",
            "",
        ):
            try:
                import numpy

                prec = int(p["numpy_precision"])
                content.append("    import numpy")
                content.append("    numpy.set_printoptions(%d)" % prec)
            except (ImportError, ValueError):
                pass

        content.append("    ## __WD__ ##")

        if p["restore"]:
            context = getattr(env, "runpython_context", None)
            for k in sorted(context):
                content.append("    {0} = globals()['__runpython__{0}']".format(k))
        else:
            context = None

        modified_content = self.modify_script_before_running("\n".join(self.content))

        if p["assert"]:
            footer = []
            assert_condition = p["assert"].split("\n")
            for cond in assert_condition:
                footer.append(f"if not({cond}):")
                footer.append(
                    f"    raise AssertionError('''Condition '{cond}' failed.''')"
                )
            modified_content += "\n\n" + "\n".join(footer)

        for line in modified_content.split("\n"):
            content.append("    " + line)

        if p["store"]:
            content.append("    for __k__, __v__ in locals().copy().items():")
            content.append("        globals()['__runpython__' + __k__] = __v__")

        if not p["process"]:
            content.append(f"{name}()")

        script = "\n".join(content)
        script_disp = "\n".join(self.content)
        if not p["noblack"]:
            try:
                script_disp = remove_extra_spaces_and_black(script_disp, is_string=True)
            except Exception as e:
                logger = logging.getLogger("runpython")
                if "." in docname:
                    comment = f'  File "{docname}", line {lineno}'
                else:
                    comment = (
                        f'  File "{docname}.rst", line {lineno}'
                        f'\n  File "{docname}.py", line {1}\n'
                    )
                logger.warning(
                    "Black (%r) issue with %r\n---SCRIPT---\n%s", e, docname, script
                )

        # if an exception is raised, the documentation should report a warning
        # return [document.reporter.warning('messagr', line=self.lineno)]
        current_source = self.state.document.current_source
        docstring = ":docstring of " in current_source
        if docstring:
            current_source = current_source.split(":docstring of ")[0]
        if os.path.exists(current_source):
            comment = f'  File "{current_source}", line {lineno}'
            if docstring:
                new_name = os.path.split(current_source)[0] + ".py"
                comment += f'\n  File "{new_name}", line {lineno}'
            cs_source = current_source
        else:
            if "." in docname:
                comment = f'  File "{docname}", line {lineno}'
            else:
                comment = (
                    '  File "{0}.rst", line {1}\n  File "{0}.py", line {1}\n'.format(
                        docname, lineno
                    )
                )
            cs_source = docname

        # Add __WD__.
        cs_source_dir = os.path.dirname(cs_source).replace("\\", "/")
        script = script.replace("## __WD__ ##", f"__WD__ = '{cs_source_dir}'")

        out, err, context = run_python_script(
            script,
            comment=comment,
            setsysvar=p["setsysvar"],
            process=p["process"],
            exception=p["exception"],
            warningout=p["warningout"],
            chdir=cs_source_dir if p["current"] else None,
            context=context,
            store_in_file=p["store_in_file"],
        )

        if p["store"]:
            # Stores modified local context.
            setattr(env, "runpython_context", context)  # noqa: B010
        else:
            context = {}
            setattr(env, "runpython_context", context)  # noqa: B010

        if out is not None:
            out = out.rstrip(" \n\r\t")
        if err is not None:
            err = err.rstrip(" \n\r\t")
        content = out
        if len(err) > 0:
            content += "\n[runpythonerror]\n" + err

        # add member
        self.exe_class = p.copy()
        self.exe_class.update(dict(out=out, err=err, script=script))

        # add indent
        def add_indent(content, nbind):
            "local function"
            lines = content.split("\n")
            if nbind > 0:
                lines = [(" " * nbind + _) for _ in lines]
            content = "\n".join(lines)
            return content

        content = add_indent(content, p["indent"])

        # build node
        node = self.__class__.runpython_class(
            rawsource=content,
            indent=p["indent"],
            showcode=p["showcode"],
            rst=p["rst"],
            sin=p["sin"],
            sout=p["sout"],
        )

        if p["showcode"]:
            if "code" in p["toggle"] or "both" in p["toggle"]:
                hide = (
                    TITLES[language_code]["hide"] + " " + TITLES[language_code]["code"]
                )
                unhide = (
                    TITLES[language_code]["unhide"]
                    + " "
                    + TITLES[language_code]["code"]
                )
                secin = collapse_node(hide=hide, unhide=unhide, show=False)
                node += secin
            else:
                secin = node
            pin = nodes.paragraph(text=p["sin"])
            if p["language"] in (None, ""):
                p["language"] = "python"
            if p["language"]:
                pcode = nodes.literal_block(
                    script_disp,
                    script_disp,
                    language=p["language"],
                    linenos=p["linenos"],
                )
            else:
                pcode = nodes.literal_block(
                    script_disp, script_disp, linenos=p["linenos"]
                )
            secin += pin
            secin += pcode

        elif len(self.options.get("sout", "")) == 0:
            p["sout"] = ""
            p["sout2"] = ""

        # RST output.
        if p["rst"]:
            settings_overrides = {}
            try:
                sett.output_encoding  # noqa: B018
            except KeyError:
                settings_overrides["output_encoding"] = "unicode"
            # try:
            #     sett.doctitle_xform
            # except KeyError:
            #     settings_overrides["doctitle_xform"] = True
            try:
                sett.warning_stream  # noqa: B018
            except KeyError:
                settings_overrides["warning_stream"] = StringIO()
            # 'initial_header_level': 2,

            secout = node
            if "out" in p["toggle"] or "both" in p["toggle"]:
                hide = (
                    TITLES[language_code]["hide"] + " " + TITLES[language_code]["outl"]
                )
                unhide = (
                    TITLES[language_code]["unhide"]
                    + " "
                    + TITLES[language_code]["outl"]
                )
                secout = collapse_node(hide=hide, unhide=unhide, show=False)
                node += secout
            elif len(p["sout"]) > 0:
                secout += nodes.paragraph(text=p["sout"])

            content_rows = content.replace("\r", "").split("\n")

            if p["debug"]:
                full_content = "\n".join(
                    f"    {i+1:05d}: {row}" for i, row in enumerate(content_rows)
                )
                content_rows.extend(["", f"*n_rows: {len(content_rows)}*"])
                for i, row in enumerate(content_rows):
                    if set(row) in ({"+"}, {"="}, {"-"}):
                        title = content_rows[i - 1]
                        content_rows.append(f"* *{i}:{title}*")
                content_rows.extend(
                    ["", "", ".. code-block:: text", "", full_content, ""]
                )

            try:
                if p["sphinx"]:
                    st = StringList(content_rows)
                    nested_parse_with_titles(self.state, st, secout)
                    dt = None
                else:
                    dt = core.publish_doctree(
                        content, settings=sett, settings_overrides=settings_overrides
                    )
            except Exception as e:
                tab = content
                content = ["::"]
                st = StringIO()
                traceback.print_exc(file=st)
                content.append("")
                trace = st.getvalue()
                trace += "\n----------------------OPT\n" + str(p)
                trace += "\n----------------------EXC\n" + str(e)
                trace += "\n----------------------SETT\n" + str(sett)
                trace += "\n----------------------ENV\n" + str(env)
                trace += "\n----------------------DOCNAME\n" + str(docname)
                trace += "\n----------------------CODE\n"
                content.extend("    " + _ for _ in trace.split("\n"))
                content.append("")
                content.append("")
                content.extend("    " + _ for _ in tab.split("\n"))
                content = "\n".join(content)
                pout = nodes.literal_block(content, content)
                secout += pout
                dt = None

            if dt is not None:
                for ch in dt.children:
                    node += ch

        # Regular output.
        if not p["rst"] or p["showout"]:
            text = p["sout2"] if p["rst"] else p["sout"]
            secout = node
            if "out" in p["toggle"] or "both" in p["toggle"]:
                hide = (
                    TITLES[language_code]["hide"] + " " + TITLES[language_code]["outl"]
                )
                unhide = (
                    TITLES[language_code]["unhide"]
                    + " "
                    + TITLES[language_code]["outl"]
                )
                secout = collapse_node(hide=hide, unhide=unhide, show=False)
                node += secout
            elif len(text) > 0:
                pout2 = nodes.paragraph(text=text)
                node += pout2
            pout = nodes.literal_block(content, content)
            secout += pout

        p["runpython"] = node

        # classes
        node["classes"] += ["runpython"]
        ns = [node]
        return ns

    def modify_script_before_running(self, script):
        """
        Takes the script as a string
        and returns another string before it is run.
        It does not modify what is displayed.
        The function can be overwritten by any class
        based on this one.
        """
        return script


def visit_runpython_node(self, node):
    """
    What to do when visiting a node :class:`runpython_node`
    the function should have different behaviour,
    depending on the format, or the setup should
    specify a different function for each.
    """
    pass


def depart_runpython_node(self, node):
    """
    What to do when leaving a node :class:`runpython_node`
    the function should have different behaviour,
    depending on the format, or the setup should
    specify a different function for each.
    """
    pass


def setup(app):
    """
    setup for ``runpython`` (sphinx)
    """
    app.add_config_value("out_runpythonlist", [], "env")
    if hasattr(app, "add_mapping"):
        app.add_mapping("runpython", runpython_node)

    app.add_node(
        runpython_node,
        html=(visit_runpython_node, depart_runpython_node),
        epub=(visit_runpython_node, depart_runpython_node),
        elatex=(visit_runpython_node, depart_runpython_node),
        latex=(visit_runpython_node, depart_runpython_node),
        rst=(visit_runpython_node, depart_runpython_node),
        md=(visit_runpython_node, depart_runpython_node),
        text=(visit_runpython_node, depart_runpython_node),
    )

    app.add_directive("runpython", RunPythonDirective)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
