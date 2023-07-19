from .runpython import run_cmd


def _check_cmd(cmd):
    try:
        stdout, _ = run_cmd(f"{cmd} --help", wait=True)
    except FileNotFoundError:
        return False
    if cmd in stdout:
        return True
    return False


def has_dvipng():
    """
    Checks `dvipng` is installed.
    """
    return _check_cmd("dvipng")


def has_dvisvgm():
    """
    Checks `dvisvgm` is installed.
    """
    return _check_cmd("dvisvgm")
