import inspect
import re
from docutils import nodes
import sphinx
from sphinx.util import logging
from sphinx.util.docfields import DocFieldTransformer, _is_single_paragraph
from ..import_object_helper import import_any_object, import_object


class Parameter:
    "Definition of a parameter."

    def __init__(self, name: str, dtype: type):
        self.name = name
        self.dtype = dtype

    def __repr__(self):
        if self.dtype is None:
            return self.name
        return f"{self.name}: {self.dtype}"


class Signature:
    "Definition of a signature."

    def __init__(self, name, result_type):
        self.name = name
        self.result_type = result_type
        self.params = []

    def append(self, par: Parameter) -> None:
        self.params.append(par)

    def __repr__(self):
        els = [self.name, "("]
        ps = []
        for p in self.params:
            ps.append(repr(p))
        els.append(", ".join(ps))
        if self.result_type is None:
            els.append(")")
        else:
            els.extend([")", " -> ", self.result_type])
        return "".join(els)

    @property
    def param_names(self):
        return set(el.name for el in self.params)


def parse_signature(text: str) -> Signature:
    if text is None:
        return None
    reg = re.compile("([_a-zA-Z][_a-zA-Z0-9]*?)[(](.*?)[)]( -> ([a-zA-Z0-9]+))?")
    try:
        res = reg.search(text)
    except TypeError as e:
        raise TypeError(f"Unexpected type {type(text)} for text.") from e
    if res is None:
        return None
    name, params, _, result = res.groups()
    spl = [_.strip() for _ in params.split(",")]
    sig = Signature(name.strip(), result.strip() if result is not None else None)
    for p in spl:
        if ":" in p:
            k, v = p.split(":", maxsplit=1)
            sig.append(Parameter(k.strip(), v.strip()))
        else:
            sig.append(Parameter(p.strip(), None))
    return sig


def check_typed_make_field(
    self,
    types,
    domain,
    items,
    env=None,
    parameters=None,
    function_name=None,
    docname=None,
    kind=None,
):
    """
    Overwrites function
    `make_field
    <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/docfields.py#L197>`_.
    Processes one argument of a function.

    :param self: from original function
    :param types: from original function
    :param domain: from original function
    :param items: from original function
    :param env: from original function
    :param parameters: list of known arguments for the function or method
    :param function_name: function name these arguments belong to
    :param docname: document which contains the object
    :param kind: tells which kind of object *function_name* is
        (function, method or class)

    Example of warnings it raises:

    ::

        [docassert] 'onefunction' has no parameter 'a'
            (in '...project_name/subproject/myexampleb.py').
        [docassert] 'onefunction' has undocumented parameters 'a, b'
            (...project_name/subproject/myexampleb.py').

    """
    if parameters is None:
        parameters = None
        check_params = {}
    else:
        parameters = list(parameters)
        if kind == "method":
            parameters = parameters[1:]

        def kg(p):
            "local function"
            return p if isinstance(p, str) else p.name

        check_params = {kg(p): 0 for p in parameters}
    logger = logging.getLogger("docassert")

    def check_item(fieldarg, content, logger):
        "local function"
        if fieldarg not in check_params:
            if function_name is not None:
                idocname = (
                    docname.replace(".PyCapsule.", ".")
                    if ".PyCapsule." in docname
                    else docname
                )
                if kind is None:
                    obj = import_any_object(idocname)
                else:
                    obj = import_object(idocname, kind=kind)
                try:
                    tsig = getattr(obj[0], "__text_signature__")  # noqa: B009
                except AttributeError:
                    tsig = "?"
                if tsig != "($self, /, *args, **kwargs)":
                    logger.warning(
                        "[docassert] %r has no parameter %r (in %r) [sig=%r]%s.",
                        function_name,
                        fieldarg,
                        docname,
                        tsig,
                        " (no detected signature) " if parameters is None else "",
                    )
        else:
            check_params[fieldarg] += 1
            if check_params[fieldarg] > 1:
                logger.warning(
                    "[docassert] %r of %r is duplicated (in %r).",
                    fieldarg,
                    function_name,
                    docname,
                )

    if isinstance(items, list):
        for fieldarg, content in items:
            check_item(fieldarg, content, logger)
        mini = None if len(check_params) == 0 else min(check_params.values())
        if mini == 0:
            check_params = list(check_params.items())
            nodoc = list(sorted(k for k, v in check_params if v == 0))
            if len(nodoc) > 0:
                if len(nodoc) == 1 and nodoc[0] == "self":
                    # Behavior should be improved.
                    pass
                else:
                    idocname = (
                        docname.replace(".PyCapsule.", ".")
                        if ".PyCapsule." in docname
                        else docname
                    )
                    if kind is None:
                        obj = import_any_object(idocname)
                    else:
                        obj = import_object(idocname, kind=kind)
                    tsig = getattr(obj[0], "__text_signature__", None)
                    if tsig != "($self, /, *args, **kwargs)":
                        if tsig is None:
                            alt_sig = parse_signature(obj[0].__doc__)
                            if alt_sig is None:
                                nodoc2 = nodoc
                            else:
                                ps = alt_sig.param_names
                                nodoc2 = [n for n in nodoc if n not in ps]
                            if len(nodoc2) > 0:
                                logger.warning(
                                    "[docassert] %r has undocumented parameters (1) "
                                    "[%s] (in %r) [sig=%r].",
                                    function_name,
                                    ", ".join(nodoc2),
                                    docname,
                                    tsig,
                                )
                        else:
                            logger.warning(
                                "[docassert] %r has undocumented parameters (2) "
                                "[%s] (in %r) [sig=%r].",
                                function_name,
                                ", ".join(nodoc),
                                docname,
                                tsig,
                            )
    else:
        # Documentation related to the return.
        pass


class OverrideDocFieldTransformer:
    """
    Overrides one function with assigning it to a method.

    :param replaced: should be `DocFieldTransformer.transform`
    """

    def __init__(self, replaced):
        self.replaced = replaced

    def override_transform(self, other_self, node):
        """
        Transform a single field list *node*.
        Overwrite function `transform
        <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/docfields.py#L271>`_.
        It only adds extra verification and returns results from
        the replaced function.

        :param other_self: the builder
        :param node: node the replaced function changes or replace

        The function parses the original function and checks that the list
        of arguments declared by the function is the same the list of
        documented arguments.
        """
        typemap = other_self.typemap
        entries = []
        groupindices = {}
        types = {}

        # step 1: traverse all fields and collect field types and content
        for field in node:
            fieldname, fieldbody = field
            try:
                # split into field type and argument
                fieldtype, fieldarg = fieldname.astext().split(None, 1)
            except ValueError:
                # maybe an argument-less field type?
                fieldtype, fieldarg = fieldname.astext(), ""
            if fieldtype == "Parameters":
                # numpydoc style
                keyfieldtype = "parameter"
            elif fieldtype == "param":
                keyfieldtype = "param"
            else:
                continue
            typedesc, is_typefield = typemap.get(keyfieldtype, (None, None))

            # sort out unknown fields
            extracted = []
            if keyfieldtype == "parameter":
                # numpydoc

                for child in fieldbody.children:
                    if isinstance(child, nodes.definition_list):
                        for child2 in child.children:
                            extracted.append(child2)
            elif typedesc is None or typedesc.has_arg != bool(fieldarg):
                # either the field name is unknown, or the argument doesn't
                # match the spec; capitalize field name and be done with it
                new_fieldname = fieldtype[0:1].upper() + fieldtype[1:]
                if fieldarg:
                    new_fieldname += " " + fieldarg
                fieldname[0] = nodes.Text(new_fieldname)
                entries.append(field)
                continue

            typename = typedesc.name

            # collect the content, trying not to keep unnecessary paragraphs
            if extracted:
                content = extracted
            elif _is_single_paragraph(fieldbody):
                content = fieldbody.children[0].children
            else:
                content = fieldbody.children

            # if the field specifies a type, put it in the types collection
            if is_typefield:
                # filter out only inline nodes; others will result in invalid
                # markup being written out
                content = [
                    n for n in content if isinstance(n, (nodes.Inline, nodes.Text))
                ]
                if content:
                    types.setdefault(typename, {})[fieldarg] = content
                continue

            # also support syntax like ``:param type name:``
            if typedesc.is_typed:
                try:
                    argtype, argname = fieldarg.split(None, 1)
                except ValueError:
                    pass
                else:
                    types.setdefault(typename, {})[argname] = [nodes.Text(argtype)]
                    fieldarg = argname

            translatable_content = nodes.inline(fieldbody.rawsource, translatable=True)
            translatable_content.document = fieldbody.parent.document
            translatable_content.source = fieldbody.parent.source
            translatable_content.line = fieldbody.parent.line
            translatable_content += content

            # Import object, get the list of parameters
            docs = fieldbody.parent.source.split("docstring of")[-1].strip()
            docs = docs.replace(".PyCapsule.", ".")

            myfunc = None
            funckind = None
            function_name = None
            excs = []
            try:
                myfunc, function_name, funckind = import_any_object(docs)
            except ImportError as e:
                excs.append(e)

            if myfunc is None:
                if len(excs) > 0:
                    reasons = "\n".join(f"   {e}" for e in excs)
                else:
                    reasons = "unknown"
                logger = logging.getLogger("docassert")
                logger.warning(
                    "[docassert] unable to import object %r, reasons: %s", docs, reasons
                )

            if myfunc is None:
                signature = None
                parameters = None
            else:
                try:
                    signature = inspect.signature(myfunc)
                    parameters = signature.parameters
                except (TypeError, ValueError):
                    # built-in function
                    logger = logging.getLogger("docassert")
                    if myfunc.__text_signature__:
                        logger.warning(
                            "[docassert] unable to get signature (1) of %r: %s",
                            docs,
                            myfunc.__text_signature__,
                        )
                        signature = None
                        parameters = None
                    else:
                        alt_sig = parse_signature(myfunc.__doc__)
                        signature = alt_sig
                        parameters = alt_sig.params

            # grouped entries need to be collected in one entry, while others
            # get one entry per field
            if extracted:
                # numpydoc
                group_entries = []
                for ext in extracted:
                    name = ext.astext().split("\n")[0].split()[0]
                    group_entries.append((name, ext))
                entries.append([typedesc, group_entries])
            elif typedesc.is_grouped:
                if typename in groupindices:
                    group = entries[groupindices[typename]]
                else:
                    groupindices[typename] = len(entries)
                    group = [typedesc, []]
                    entries.append(group)
                entry = typedesc.make_entry(fieldarg, [translatable_content])
                group[1].append(entry)
            else:
                entry = typedesc.make_entry(fieldarg, [translatable_content])
                entries.append([typedesc, entry])

        # step 2: all entries are collected, check the parameters list.
        try:
            env = other_self.directive.state.document.settings.env
        except AttributeError as e:
            logger = logging.getLogger("docassert")
            logger.warning("[docassert] %s", e)
            env = None

        docname = fieldbody.parent.source.split("docstring of")[-1].strip()

        for entry in entries:
            if isinstance(entry, nodes.field):
                logger = logging.getLogger("docassert")
                logger.warning("[docassert] unable to check [nodes.field] %s", entry)
            else:
                fieldtype, content = entry
                fieldtypes = types.get(fieldtype.name, {})
                check_typed_make_field(
                    other_self,
                    fieldtypes,
                    other_self.directive.domain,
                    content,
                    env=env,
                    parameters=parameters,
                    function_name=function_name,
                    docname=docname,
                    kind=funckind,
                )

        return self.replaced(other_self, node)


def setup_docassert(app):
    """
    setup for ``docassert`` extension (sphinx).
    This changes ``DocFieldTransformer.transform`` and replaces
    it by a function which calls the current function and does
    extra checking on the list of parameters.

    .. warning:: This class does not handle methods if the parameter name
        for the class is different from *self*. Classes included in other
        classes are not properly handled.
    """
    inst = OverrideDocFieldTransformer(DocFieldTransformer.transform)

    def local_transform(me, node):
        "local function"
        return inst.override_transform(me, node)

    DocFieldTransformer.transform = local_transform
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}


def setup(app):
    "setup for docassert"
    return setup_docassert(app)
