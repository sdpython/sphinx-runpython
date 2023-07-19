from .runpython import run_cmd


def _check_cmd(cmd):
    stdout, _ = run_cmd(f"{cmd} --help", wait=True)
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
