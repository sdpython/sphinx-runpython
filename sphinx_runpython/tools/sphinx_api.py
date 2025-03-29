import os
import textwrap
from typing import Dict, List, Optional


def _write_doc_folder(
    folder: str,
    pyfiles: List[str],
    hidden: bool = False,
    prefix: str = "",
    subfolders: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Creates all the file in a dictionary.
    """
    template = textwrap.dedent(
        """
    <full_module_name>
    <line>

    .. automodule:: <full_module_name>
        :members:
        :no-undoc-members:
    """
    )

    index = textwrap.dedent(
        """
    <full_module_name>
    <line>
    """
    )

    submodule = ".".join(os.path.splitext(folder)[0].replace("\\", "/").split("/"))
    fullsubmodule = f"{prefix}.{submodule}" if prefix else submodule
    rows = [
        index.replace("<submodule>", submodule)
        .replace("<full_module_name>", fullsubmodule)
        .replace("<line>", "=" * len(fullsubmodule)),
    ]
    if subfolders:
        rows.append(
            textwrap.dedent(
                """
        .. toctree::
            :maxdepth: 1
            :caption: submodules

        """
            )
        )
        for sub in subfolders:
            rows.append(f"    {sub}/index")
    res = {}
    has_module = False
    for name in sorted(pyfiles):
        if not name:
            continue
        module_name = ".".join(os.path.splitext(name)[0].replace("\\", "/").split("/"))
        last = module_name.split(".")[-1]
        if not hidden and last[0] == "_" and last != "__init__":
            continue
        if not module_name or module_name in ("__main__", "__init__"):
            continue
        key = f"{module_name}.rst"
        if module_name.endswith("__init__"):
            module_name = ".".join(module_name.split(".")[:-1])
        full_module_name = f"{submodule}.{module_name}"
        line = "=" * len(full_module_name)
        text = (
            template.replace("<module_name>", module_name)
            .replace("<full_module_name>", full_module_name)
            .replace("<line>", line)
        )
        res[key] = text
        if not has_module:
            has_module = True
            rows.append(
                textwrap.dedent(
                    """

            .. toctree::
                :maxdepth: 1
                :caption: modules

            """
                )
            )
        rows.append(f"    {last}")

    rows.append(
        textwrap.dedent(
            f"""

    .. automodule:: {submodule}
        :members:
        :no-undoc-members:
    """
        )
    )
    res["index.rst"] = "\n".join(rows)
    return res


def sphinx_api(
    folder: str,
    output_folder: Optional[str] = None,
    simulate: bool = False,
    hidden: bool = False,
    verbose: int = 0,
):
    """
    Creates simple pages to document a package.
    Relies on :epkg:`automodule`.

    :param folder: folder to document
    :param output_folder: where to write the result
    :param simulate: prints out what the function will do
    :param hidden: document file starting with `_`
    :param verbose: verbosity
    :return: list of written file
    """
    folder = folder.rstrip("/\\")
    root, package_name = os.path.split(folder)
    files = []
    if verbose:
        print(f"[sphinx_api] start creating API for {folder!r}")

    for racine, dossiers, fichiers in os.walk(folder):
        pyfiles = [f for f in fichiers if f.endswith(".py")]
        if not pyfiles:
            continue
        mname = racine[len(root) + 1 :] if root else racine
        selected = [
            d
            for d in dossiers
            if os.path.exists(os.path.join(racine, d, "__init__.py"))
        ]
        if verbose:
            print(f"[sphinx_api] open {mname!r}")
            if selected:
                print(f"[sphinx_api]    submodules {selected!r}")
        content = _write_doc_folder(
            mname, pyfiles, hidden=hidden, prefix="", subfolders=selected
        )
        if verbose:
            print(f"[sphinx_api] close {mname!r}")
        if simulate:
            print(f"--+ {mname}")
            for k, _v in content.items():
                print(f"  | {k}")
        else:
            assert output_folder, "output_folder is empty"
            subfolder = os.path.join(output_folder, *mname.split("/")[1:])
            if verbose:
                print(f"[sphinx_api] create {subfolder!r}")
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)
            for k, v in content.items():
                n = os.path.join(subfolder, k)
                if verbose:
                    print(f"[sphinx_api] write {n!r}")
                with open(n, "w") as f:
                    f.write(v)
                files.append(n)
    return files
