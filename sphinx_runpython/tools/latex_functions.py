import re
from typing import Dict, Optional, Tuple, Union

PREAMBLE = """
\\newcommand{\\vecteurno}[2]{#1,\\dots,#2}
\\newcommand{\\R}{\\mathbb{R}}
\\newcommand{\\pa}[1]{\\left(#1\\right)}
\\newcommand{\\cro}[1]{\\left[#1\\right]}
\\newcommand{\\acc}[1]{\\left\\{#1\\right\\}}
\\newcommand{\\vecteur}[2]{\\left(#1,\\dots,#2\\right)}
\\newcommand{\\N}[0]{\\mathbb{N}}
\\newcommand{\\indicatrice}[1]{ {1\\!\\!1}_{\\left\\{#1\\right\\}} }
\\newcommand{\\infegal}[0]{\\leqslant}
\\newcommand{\\supegal}[0]{\\geqslant}
\\newcommand{\\ensemble}[2]{\\left\\{#1,\\dots,#2\\right\\}}
\\newcommand{\\fleche}[1]{\\overrightarrow{#1}}
\\newcommand{\\intervalle}[2]{\\left\\{#1,\\cdots,#2\\right\\}}
\\newcommand{\\independent}[0]{\\perp \\!\\!\\! \\perp}
\\newcommand{\\esp}{\\mathbb{E}}
\\newcommand{\\espf}[2]{\\mathbb{E}_{#1}\\left(#2\\right)}
\\newcommand{\\var}{\\mathbb{V}}
\\newcommand{\\pr}[1]{\\mathbb{P}\\left(#1\\right)}
\\newcommand{\\loi}[0]{{\\cal L}}
\\newcommand{\\norm}[1]{\\left\\Vert#1\\right\\Vert}
\\newcommand{\\norme}[1]{\\left\\Vert#1\\right\\Vert}
\\newcommand{\\scal}[2]{\\left<#1,#2\\right>}
\\newcommand{\\dans}[0]{\\rightarrow}
\\newcommand{\\partialfrac}[2]{\\frac{\\partial #1}{\\partial #2}}
\\newcommand{\\partialdfrac}[2]{\\dfrac{\\partial #1}{\\partial #2}}
\\newcommand{\\trace}[1]{tr\\left(#1\\right)}
\\newcommand{\\sac}[0]{|}
\\newcommand{\\abs}[1]{\\left|#1\\right|}
\\newcommand{\\loinormale}[2]{{\\cal N} \\left(#1,#2\\right)}
\\newcommand{\\loibinomialea}[1]{{\\cal B} \\left(#1\\right)}
\\newcommand{\\loibinomiale}[2]{{\\cal B} \\left(#1,#2\\right)}
\\newcommand{\\loimultinomiale}[1]{{\\cal M} \\left(#1\\right)}
\\newcommand{\\variance}[1]{\\mathbb{V}\\left(#1\\right)}
\\newcommand{\\intf}[1]{\\left\\lfloor #1 \\right\\rfloor}
"""


def build_regex(text: Optional[str] = None) -> Dict[str, Union[str, Tuple[str, str]]]:
    """
    Parses a preamble in latex and builds regular expressions
    based on it.
    """
    if text is None:
        text = PREAMBLE
    lines = [_ for _ in text.split("\n") if "newcommand" in _]
    reg = re.compile(r"newcommand\{\\([a-zA-Z]+)\}(\[([0-9])\])?\{(.+)\}")
    res = {}
    for i, line in enumerate(lines):
        match = reg.search(line)
        assert match, f"Unable to match pattern reg={reg} in line {i}: {line!r}"
        name, n, pat = match.group(1), match.group(3), match.group(4)
        if n is None or int(n) == 0:
            res[name] = pat
        elif name in {"pa", "cro", "acc", "abs"}:
            # These can be nested expression.
            spl = line.split("#1")
            begin, end = spl[0][-1], spl[-1][-2]
            if begin == "{":
                begin = "\\{"
            if end == "}":
                end = "\\}"
            res[name] = (
                lambda s, name=name, begin=begin, end=end: replace_nested_bracked(
                    s, name=name, begin=begin, end=end
                )
            )
        else:
            look = f"\\\\{name} *" + "\\{(.+?)\\}" * int(n)
            for c in "\\":
                pat = pat.replace(c, f"\\{c}")
            for k in range(int(n)):
                pat = pat.replace(f"#{k+1}", f"\\{k+1}")
            res[name] = (look, pat)
    return res


def replace_nested_bracked(text: str, name: str, begin: str, end: str) -> str:
    """
    Replaces brackets, nested brackets...
    """
    find_left = f"\\{name}" + "{"
    if find_left not in text:
        return text
    content = [[]]
    i = 0
    while i < len(text):
        if i + len(find_left) < len(text) and text[i : i + len(find_left)] == find_left:
            content.append([])
            content[-1].append(f"\\left{begin}")
            i += len(find_left)
        elif text[i] == "{":
            content.append([])
            content[-1].append(text[i])
            i += 1
        elif text[i] == "}":
            content[-1].append(
                f"\\right{end}" if content[-1][0].startswith("\\left") else text[i]
            )
            content[-2].append("".join(content.pop()))
            i += 1
        else:
            content[-1].append(text[i])
            i += 1
    return "".join(content[0])


def replace_latex_command(
    text: str,
    patterns: Optional[Dict[str, Union[str, Tuple[str, str]]]] = None,
    verbose: int = 0,
) -> str:
    """
    Replaces a latex by its raw expression.

    :param text: text
    :param patterns: one in the known list or None for all
    :param verbose: verbosity
    :return: modified text

    The default patterns are defined by:

    .. runpython::
        :showcode:

        from sphinx_runpython.tools.latex_functions import PREAMBLE

        print(PREAMBLE)

    With gives:

    .. runpython::
        :showcode:

        import pprint
        from sphinx_runpython.tools.latex_functions import build_regex

        pprint.pprint(build_regex())
    """
    if patterns is None:
        patterns = build_regex()

    for k, v in patterns.items():
        if verbose:
            text0 = text
        if isinstance(v, str):
            text = text.replace(f"\\{k}", v)
            if verbose and text != text0:
                print(f"[replace_latex_command] (1) {k!r}:[{text0}] -> [{text}]")
        elif isinstance(v, tuple) and len(v) == 2:
            try:
                text = re.sub(v[0], v[1], text)
            except re.error as e:
                raise AssertionError(
                    f"Unable to replace pattern {v[0]!r} by {v[1]!r} for text={text!r}"
                ) from e
            if verbose and text != text0:
                print(f"[replace_latex_command] (2) {k!r}:[{text0}] -> [{text}]")
        elif callable(v):
            text = v(text)
            if verbose and text != text0:
                print(f"[replace_latex_command] (3) {k!r}:[{text0}] -> [{text}]")
        else:
            raise AssertionError(f"Unable to understand v={v!r} for k={k!r}")
    return text
