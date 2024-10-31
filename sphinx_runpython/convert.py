import json
from typing import Optional
import pypandoc as pdoc


def convert_ipynb_to_gallery(nbfile: str, outfile: Optional[str] = None) -> str:
    """
    Convert jupyter notebook to sphinx gallery notebook styled examples.
    It relies on :epkg:`pypandoc`.
    Inspired from `ipynb_to_gallery.py
    <https://gist.github.com/chsasank/7218ca16f8d022e02a9c0deb94a310fe>`_.

    :param nbfile: notebook file
    :param outfile: outpitfile
    :return: content of this output file
    """
    python_file = []

    with open(nbfile, "r", encoding="utf-8") as f:
        nb_dict = json.load(f)
    cells = nb_dict["cells"]

    for i, cell in enumerate(cells):
        if i == 0:
            if cell["cell_type"] != "markdown":
                raise ValueError(
                    f"First cell has to be markdown but is {cell['cell_type']!r}."
                )

            md_source = "".join(cell["source"])
            rst_source = pdoc.convert_text(md_source, "rst", "md")
            python_file.append('"""\n' + rst_source + '\n"""')
        else:
            if cell["cell_type"] == "markdown":
                md_source = "".join(cell["source"])
                rst_source = pdoc.convert_text(md_source, "rst", "md")
                commented_source = "\n".join(["# " + x for x in rst_source.split("\n")])
                python_file.append("\n\n\n" + "#" * 70 + "\n" + commented_source)
            elif cell["cell_type"] == "code":
                source = "".join(cell["source"])
                python_file.append("\n" * 2 + source)

    python_file = "".join(python_file)

    python_file = python_file.replace("\n%", "\n# %")
    python_file = python_file.replace("’", "'")  # noqa: RUF001
    python_file = python_file.replace("# %matplotlib inline", "")
    python_file = python_file.replace("# \n", "\n")
    python_file = python_file.replace(">`__", ">`_")
    if outfile is None:
        return python_file
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(python_file)
