import os
import sys
from typing import Any, Dict, List, Optional
from urllib.request import urlretrieve


class VirtualEnvError(Exception):
    """
    Exception raised by the function implemented in this file.
    """

    pass


class NotImplementedErrorFromVirtualEnvironment(NotImplementedError):
    """
    Defines an exception when a function does not work
    in a virtual environment.
    """

    pass


def is_virtual_environment() -> bool:
    """
    Tells if the script is run from a virtual environment.
    """
    return (
        getattr(sys, "base_exec_prefix", sys.exec_prefix) != sys.exec_prefix
    ) or hasattr(sys, "real_prefix")


def build_venv_cmd(params: Dict[str, Any], posparams: List[Any]) -> str:
    """
    Builds the command line for virtual env.

    :param params: dictionary of parameters
    :param posparams: positional arguments
    :return: string
    """
    import venv

    v = venv.__file__
    if v is None:
        raise ImportError("module venv should have a version number")
    exe = sys.executable.replace("w.exe", "").replace(".exe", "")
    cmd = [exe, "-m", "venv"]
    for k, v in params.items():
        if v is None:
            cmd.append("--" + k)
        else:
            cmd.append("--" + k + "=" + v)
    cmd.extend(posparams)
    return " ".join(cmd)


def create_virtual_env(
    where: str,
    symlinks: bool = False,
    system_site_packages: bool = False,
    clear: bool = True,
    packages: Optional[List[str]] = None,
    verbose: int = 0,
    temp_folder: Optional[str] = None,
    platform: Optional[str] = None,
) -> str:
    """
    Creates a virtual environment.

    :param where: location of this virtual environment
    :param symlinks: attempt to symlink rather than copy
    :param system_site_packages: Give the virtual environment
        access to the system site-packages dir
    :param clear: Delete the environment directory if it already exists.
        If not specified and the directory exists, an error is raised.
    :param packages: list of packages to install
    :param temp_folder: temporary folder (to download module if needed),
        by default ``<where>/download``
    :param platform: platform to use
    :param verbose: verbosity
    :return: standard output

    .. faqref::
        :title: How to create a virtual environment?

        The following example creates a virtual environment.
        Packages can be added by specifying the parameter *package*.

        ::

            import os
            from sphinx_runpython.readme import create_virtual_env

            fold = "my_env"
            if not os.path.exists(fold):
                os.mkdir(fold)
            create_virtual_env(fold)

    The function does not work from a virtual environment.
    """
    from .runpython import run_cmd

    if is_virtual_environment():
        raise NotImplementedErrorFromVirtualEnvironment()

    if verbose > 0:
        print(f"[create_virtual_env] create virtual environment at {where!r}")
    params = {}
    if symlinks:
        params["symlinks"] = None
    if system_site_packages:
        params["system-site-packages"] = None
    if clear:
        params["clear"] = None
    cmd = build_venv_cmd(params, [where])
    out, err = run_cmd(cmd, wait=True, logf=print if verbose else None)
    if len(err) > 0:
        raise VirtualEnvError(
            f"Unable to create virtual environment at {where!r}"
            f"\nCMD:\n{cmd}\nOUT:\n{out}\n[pyqerror]\n{err}"
        )

    if platform is None:
        platform = sys.platform
    if platform.startswith("win"):
        scripts = os.path.join(where, "Scripts")
    else:
        scripts = os.path.join(where, "bin")

    if not os.path.exists(scripts):
        files = "\n  ".join(os.listdir(where))
        raise FileNotFoundError(f"Unable to find {files}, content:\n  {scripts}")

    in_scripts = os.listdir(scripts)
    pips = [_ for _ in in_scripts if _.startswith("pip")]
    if len(pips) == 0:
        out += venv_install(
            where, "pip", verbose=verbose, temp_folder=temp_folder, platform=platform
        )
    in_scripts = os.listdir(scripts)
    pips = [_ for _ in in_scripts if _.startswith("pip")]
    if len(pips) == 0:
        raise FileNotFoundError(
            f"Unable to find pip in {in_scripts!r}, content:\n  {scripts}"
        )

    out += venv_install(
        where, "pip", verbose=verbose, temp_folder=temp_folder, platform=platform
    )

    if packages is not None and len(packages) > 0:
        if verbose > 0:
            print(f"[create_virtual_env] install packages in {where}")
        packages = [_ for _ in packages if _ not in ("pip",)]
        if len(packages) > 0:
            out += venv_install(
                where,
                packages,
                verbose=verbose,
                temp_folder=temp_folder,
                platform=platform,
            )
    return out


def venv_install(
    venv: str,
    packages: List[str],
    verbose: int = 0,
    temp_folder: Optional[str] = None,
    platform: Optional[str] = None,
) -> str:
    """
    Installs a package or a list of packages in a virtual environment.

    :param venv: location of the virtual environment
    :param packages: a package (str) or a list of packages(list[str])
    :param temp_folder: temporary folder (to download module if needed),
        by default ``<where>/download``
    :param platform: platform (``sys.platform`` by default)
    :param verbose: verbosity
    :return: standard output

    The function does not work from a virtual environment.
    """
    from .runpython import run_cmd

    if is_virtual_environment():
        raise NotImplementedErrorFromVirtualEnvironment()
    if temp_folder is None:
        temp_folder = os.path.join(venv, "download")
    if isinstance(packages, str):
        packages = [packages]
    if platform is None:
        platform = sys.platform

    exe = os.path.join(venv, "bin", "python")
    get_pip = os.path.join(venv, "get_pip.py")
    if packages == "pip" or packages == ["pip"]:
        if not os.path.exists(get_pip):
            if verbose > 2:
                print("[bench_virtual] install pip")
            urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip)
        cmd = [exe, get_pip]
        out, err = run_cmd([exe, get_pip], wait=True)
    else:
        pcks = " ".join(packages)
        cmd = f"{exe} -m pip install {pcks}"
        out, err = run_cmd(cmd, wait=True)

    lines = [
        _
        for _ in err.split("\n")
        if "requires" not in _
        and "pip's dependency resolver does not currently " not in _
    ]
    err = "\n".join(lines)
    if len(err) > 0:
        raise RuntimeError(
            f"Unable to run cmd={cmd!r} in {venv!r} "
            f"(path={get_pip!r}) due to\n{err}"
        )
    if verbose > 2:
        print(out)
    return out


def run_venv_script(
    venv: str,
    script: str,
    verbose: int = 0,
    is_file: bool = False,
    is_cmd: bool = False,
    skip_err_if: Optional[bool] = None,
    platform: Optional[str] = None,
    **kwargs: Dict[str, Any],
) -> str:
    """
    Runs a script on a virtual environment (the script should be simple).

    :param venv: virtual environment
    :param script: script as a string (not a file)
    :param is_file: is script a file or a string to execute
    :param is_cmd: if True, script is a command line to run
        (as a list) for python executable
    :param skip_err_if: do not pay attention to standard
        error if this string was found in standard output
    :param platform: platform (``sys.platform`` by default)
    :param verbose: verbosity
    :param kwargs: others arguments for function @see fn run_cmd.
    :return: output

    The function does not work from a virtual environment.
    """
    from .runpython import run_cmd

    def filter_err(err):
        lis = err.split("\n")
        lines = []
        for li in lis:
            if "missing dependencies" in li:
                continue
            if "' misses '" in li:
                continue
            lines.append(li)
        return "\n".join(lines).strip(" \r\n\t")

    if is_virtual_environment():
        raise NotImplementedErrorFromVirtualEnvironment()

    if platform is None:
        platform = sys.platform

    if platform.startswith("win"):
        exe = os.path.join(venv, "Scripts", "python")
    else:
        exe = os.path.join(venv, "bin", "python")
    if is_cmd:
        cmd = " ".join([exe, *script])
        out, err = run_cmd(cmd, wait=True, logf=print if verbose else None, **kwargs)
        err = filter_err(err)
        if len(err) > 0 and (skip_err_if is None or skip_err_if not in out):
            raise VirtualEnvError(
                "unable to run cmd at {2}\n--CMD--\n{3}\n--OUT--\n{0}\n[pyqerror]"  # noqa: UP030
                "\n{1}".format(out, err, venv, cmd)
            )
        return out

    script = ";".join(script.split("\n"))
    if is_file:
        if not os.path.exists(script):
            raise FileNotFoundError(script)
        cmd = " ".join([exe, "-u", f'"{script}"'])
    else:
        cmd = " ".join([exe, "-u", "-c", f'"{script}"'])
    out, err = run_cmd(cmd, wait=True, logf=print if verbose else None, **kwargs)
    err = filter_err(err)
    if len(err) > 0:
        raise VirtualEnvError(
            f"Unable to run script at {venv!r}\n--CMD--\n{cmd}\n--OUT--\n{out}\n"
            f"[pyqerror]\n{err}"
        )
    return out


def run_base_script(
    script: str,
    is_file: bool = False,
    is_cmd: bool = False,
    verbose: int = 0,
    skip_err_if: Optional[bool] = None,
    argv: Optional[List[str]] = None,
    platform: Optional[str] = None,
    **kwargs: Dict[str, Any],
) -> str:
    """
    Runs a script with the original interpreter even if this function
    is run from a virtual environment.

    :param script: script as a string (not a file)
    :param is_file: is script a file or a string to execute
    :param is_cmd: if True, script is a command line to run
        (as a list) for python executable
    :param skip_err_if: do not pay attention to standard error
        if this string was found in standard output
    :param argv: list of arguments to add on the command line
    :param platform: platform (``sys.platform`` by default)
    :param kwargs: others arguments for function @see fn run_cmd.
    :param verbose: verbosity
    :return: output

    The function does not work from a virtual environment.
    The function does not raise an exception if the standard error
    contains something like::

        ----------------------------------------------------------------------
        Ran 1 test in 0.281s

        OK
    """
    from ..loghelper import run_cmd

    def true_err(err):
        if "Ran 1 test" in err and "OK" in err:
            return False
        return True

    if platform is None:
        platform = sys.platform

    if hasattr(sys, "real_prefix"):
        exe = sys.base_prefix
    elif hasattr(sys, "base_exec_prefix"):
        exe = sys.base_exec_prefix
    else:
        exe = sys.exec_prefix

    if platform.startswith("win"):
        exe = os.path.join(exe, "python")
    else:
        exe = os.path.join(exe, "bin", "python%d.%d" % sys.version_info[:2])
        if not os.path.exists(exe):
            exe = os.path.join(exe, "bin", "python")

    if is_cmd:
        cmd = " ".join([exe, *script])
        if argv is not None:
            cmd += " " + " ".join(argv)
        out, err = run_cmd(cmd, wait=True, verbose=verbose, **kwargs)
        if (
            len(err) > 0
            and (skip_err_if is None or skip_err_if not in out)
            and true_err(err)
        ):
            p = sys.base_prefix if hasattr(sys, "base_prefix") else sys.prefix
            raise VirtualEnvError(
                f"Unable to run cmd at {p!r}\nCMD:\n{cmd}"
                f"\nOUT:\n{out}\n[pyqerror]\n{err}"
            )
        return out

    script = ";".join(script.split("\n"))
    if is_file:
        if not os.path.exists(script):
            raise FileNotFoundError(script)
        cmd = " ".join([exe, "-u", f'"{script}"'])
    else:
        cmd = " ".join([exe, "-u", "-c", f'"{script}"'])
    if argv is not None:
        cmd += " " + " ".join(argv)
    out, err = run_cmd(cmd, wait=True, verbose=verbose, **kwargs)
    if len(err) > 0 and true_err(err):
        p = sys.base_prefix if hasattr(sys, "base_prefix") else sys.prefix
        raise VirtualEnvError(
            f"Unable to run script at {p!r}\nCMD:\n{cmd}"
            f"\nOUT:\n{out}\n[pyqerror]\n{err}"
        )
    return out


def check_readme_syntax(
    readme: str, folder: str, version: Optional[str] = None, verbose: int = 0
) -> str:
    """
    Checks the syntax of the file ``readme.rst``
    which describes a python project.

    :param readme: file to check
    :param folder: location for the virtual environment
    :param version: version of docutils
    :param verbose: verbosity
    :return: output or SyntaxError exception
    """
    if is_virtual_environment():
        raise NotImplementedErrorFromVirtualEnvironment()
    if not os.path.exists(folder):
        os.makedirs(folder)

    out = create_virtual_env(
        folder,
        verbose=verbose,
        packages=["docutils" if version is None else f"docutils=={version}"],
    )
    outfile = os.path.join(folder, "conv_readme.html")

    script = [
        "from docutils import core",
        "import io",
        "from docutils.readers.standalone import Reader",
        "from docutils.parsers.rst import Parser",
        "from docutils.parsers.rst.directives.images import Image",
        "from docutils.parsers.rst.directives import _directives",
        "from docutils.writers.html4css1 import Writer",
        "_directives['image'] = Image",
        "with open('{0}', 'r', encoding='utf8') as g: "  # noqa: UP030
        "s = g.read()".format(readme.replace("\\", "\\\\")),
        "settings_overrides = {'output_encoding': 'unicode', 'doctitle_xform': True,",
        "            'initial_header_level': 2, 'warning_stream': io.StringIO()}",
        "parts = core.publish_parts(source=s, parser=Parser(), "
        "            reader=Reader(), source_path=None,",
        "            destination_path=None, writer=Writer(),",
        "            settings_overrides=settings_overrides)",
        "with open('{0}', 'w', encoding='utf8') as f: "  # noqa: UP030
        "f.write(parts['whole'])".format(outfile.replace("\\", "\\\\")),
    ]

    file_script = os.path.join(folder, "test_" + os.path.split(readme)[-1])
    with open(file_script, "w") as f:
        f.write("\n".join(script))

    out = run_venv_script(folder, file_script, verbose=verbose, is_file=True)
    with open(outfile, "r", encoding="utf8") as h:
        content = h.read()

    if "System Message" in content:
        raise SyntaxError(
            f"Unable to parse a file with docutils=={version!r}"
            f"\n------\n{out}\n------\nCONTENT:\n{content}"
        )

    return out
