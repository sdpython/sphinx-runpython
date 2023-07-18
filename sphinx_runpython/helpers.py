from contextlib import redirect_stderr
import io
from typing import Any, Dict, Optional, Tuple
from docutils.core import publish_parts


def rst2html(
    rst: str,
    directives: Optional[Dict[str, Any]],
    report_level: int = 0,
    writer_name: str = "html",
    **kwargs
) -> Tuple[str, str]:
    """
    Converts a RST string into HTML or RST (simplified with no sphinx directives).

    :param rst: RST string
    :param directives: directives to load or None for all
        implemented in this package
    :param report_level: filter output, 0 means everything
    :param writer_name: writer name    
    :param kwargs: additional values to add to the configuration
    :return: output and warnings
    """
    docutils_kwargs = {
        "writer_name": writer_name,
        "settings_overrides": {
            "_disable_config": True,
            "report_level": report_level,
        },
    }
    target = io.StringIO()
    with redirect_stderr(target):
        parts = publish_parts(rst, **docutils_kwargs)
        html = parts["html_body"]
        warning = target.getvalue().strip()
        return html, warning
