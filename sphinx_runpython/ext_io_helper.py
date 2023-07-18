import datetime
import gzip
import os
import re
import shutil
import socket
import time
import warnings
import http.client as http_client
import urllib.error as urllib_error
import urllib.request as urllib_request
from logging import getLogger
from http.client import InvalidURL
from typing import Optional, List, Union

logger = getLogger("sphinx-runpython")


class ReadUrlException(InvalidURL):
    pass


class InternetException(IOError):
    pass


class FileException(OSError):
    pass


MONTH_DATE = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _first_more_recent(f1: str, path: str) -> bool:
    """
    Checks if the first file (opened url)
    is more recent of the second file (path).

    :param f1: opened url
    :param path: path name
    :return: True if more recent
    """
    s = str(f1.info())
    da = re.compile("Last[-]Modified: (.+) GMT").search(s)
    if da is None:
        return True
    else:  # pragma: no cover
        da = da.groups()[0]
        gr = re.compile(
            "[\\w, ]* ([ \\d]{2}) ([\\w]{3}) ([\\d]{4}) "
            "([\\d]{2}):([\\d]{2}):([\\d]{2})"
        ).search(da)
        if gr is None:
            return True
        gr = gr.groups()
        dau = datetime.datetime(
            int(gr[2]),
            MONTH_DATE[gr[1].lower()],
            int(gr[0]),
            int(gr[3]),
            int(gr[4]),
            int(gr[5]),
        )

        p = time.ctime(os.path.getmtime(path))
        gr = re.compile(
            "[\\w, ]* ([\\w]{3}) ([ \\d]{2}) ([\\d]{2}):([\\d]{2}):"
            "([\\d]{2}) ([\\d]{4})"
        ).search(p)
        if gr is None:
            return True
        gr = gr.groups()
        da = datetime.datetime(
            int(gr[5]),
            MONTH_DATE[gr[0].lower()],
            int(gr[1]),
            int(gr[2]),
            int(gr[3]),
            int(gr[4]),
        )

        file = da
        return dau > file


def _get_file_url(url: str, path: Optional[str]) -> str:
    """
    Builds a filename knowing an url.

    :param url: url
    :param path: where to download the file
    :return: filename
    """
    path = (
        path
        + "/"
        + url.replace("/", "!")
        .replace(":", "")
        .replace(".", "-")
        .replace("=", "_")
        .replace("?", "_")
    )
    spl = path.split("-")
    if len(spl) >= 2:
        ext = spl[len(spl) - 1].lower()
        if 2 <= len(ext) <= 3 and ext in {
            "c",
            "cc",
            "cpp",
            "cu",
            "gif",
            "gz",
            "h",
            "hpp",
            "html",
            "png",
            "jpeg",
            "jpg",
            "pdf",
            "py",
            "tif",
            "txt",
            "zip",
        }:
            spl = path.split("-")
            spl = spl[: len(spl) - 1]
            path = "-".join(spl) + "." + ext
    return path


def read_url(url: str, encoding: Optional[str] = None) -> Union[bytes, str]:
    """
    Reads the content of a url.

    :param url: url
    :param encoding: if None, the result type is bytes, str otherwise
    :return: str (encoding is not None) or bytes
    """
    request = urllib_request.Request(url)
    try:
        with urllib_request.urlopen(request) as fu:
            content = fu.read()
    except Exception as e:
        import urllib.parse as urlparse

        res = urlparse.urlparse(url)
        raise ReadUrlException(f"unable to open url '{url}' scheme: {res}\nexc: {e}")

    if encoding is None:
        return content
    else:
        return content.decode(encoding=encoding)


def download(url: str, path_download: str = ".", outfile: Optional[str] = None) -> str:
    """
    Downloads a small file.
    If *url* is an url, it downloads the file and returns the downloaded filename.
    If it has already been downloaded, it is not downloaded again
    The function raises an exception if the url does not contain
    ``http://`` or ``https://`` or ``ftp://``.

    :param url: url
    :param path_download: download the file here
    :param outfile: see below
    :return: the filename

    If *outfile* is None, the function will give a relative name
    based on the last part of the url.
    If *outfile* is "", the function will remove every weird character.
    If *outfile* is not null, the function will use it. It will be relative to
    the current folder and not *path_download*.
    """
    lurl = url.lower()
    if lurl.startswith("file://"):
        if outfile is None:
            last = os.path.split(url)[-1]
            if last.startswith("__cached__"):
                last = last[len("__cached__") :]
            dest = os.path.join(path_download, last)
        elif outfile == "":
            dest = _get_file_url(url, path_download)
        else:
            dest = outfile

        shutil.copy(url[7:], dest)
        return dest

    if "http://" in lurl or "https://" in lurl or "ftp://" in lurl:
        if outfile is None:
            dest = os.path.join(path_download, os.path.split(url)[-1])
        elif outfile == "":
            dest = _get_file_url(url, path_download)
        else:
            dest = outfile

        down = False
        nyet = dest + ".notyet"

        if os.path.exists(dest) and not os.path.exists(nyet):
            try:
                f1 = urllib_request.urlopen(url)
                down = _first_more_recent(f1, dest)
                newdate = down
                f1.close()
            except urllib_error.HTTPError as e:
                raise ReadUrlException(f"Unable to fetch '{url}'") from e
            except IOError as e:
                raise ReadUrlException(f"Unable to download '{url}'") from e
        else:
            down = True
            newdate = False

        if down:
            if newdate:
                logger.info("[download] downloading (updated) %r", url)
            else:
                logger.info("[download] downloading %r", url)

            if len(url) > 4 and url[-4].lower() in [
                ".txt",
                ".csv",
                ".tsv",
                ".log",
                ".tmpl",
            ]:
                logger.info("creating text file %r", dest)
                format = "w"
            else:
                logger.info("creating binary file %r", dest)
                format = "wb"

            if os.path.exists(nyet):
                size = os.stat(dest).st_size
                logger.info(
                    "[download] resume downloading (stop at %d) from %r", size, url
                )
                try:
                    request = urllib_request.Request(url)
                    request.add_header("Range", "bytes=%d-" % size)
                    fu = urllib_request.urlopen(request)
                except urllib_error.HTTPError as e:
                    raise ReadUrlException(f"Unable to fetch '{url}'") from e
                f = open(
                    dest, format.replace("w", "a")  # pylint: disable=W1501
                )  # pylint: disable=W1501
            else:
                logger.info("[download] downloading %r", url)
                try:
                    request = urllib_request.Request(url)
                    fu = urllib_request.urlopen(url)
                except urllib_error.HTTPError as e:
                    raise ReadUrlException(f"Unable to fetch '{url}'") from e
                f = open(dest, format)

            open(nyet, "w").close()
            c = fu.read(2**21)
            size = 0
            while len(c) > 0:
                size += len(c)
                logger.info("[download]    size %d", size)
                f.write(c)
                f.flush()
                c = fu.read(2**21)
            logger.info("end downloading")
            f.close()
            fu.close()
            os.remove(nyet)

        url = dest
        return url
    else:
        raise FileException(f"This url does not seem to be one {url!r}.")


def get_url_content_timeout(
    url: str,
    timeout: int = 10,
    output: Optional[str] = None,
    encoding: str = "utf-8",
    raise_exception: bool = True,
    chunk: Optional[int] = None,
) -> Union[bytes, str]:
    """
    Downloads a file from internet (by default, it assumes
    it is text information, otherwise, encoding should be None).

    :param url: url
    :param timeout: in seconds, after this time,
        the function drops an returns None, -1 for forever
    :param output: if None, the content is stored in that file
    :param encoding: utf-8 by default, but if it is None,
        the returned information is binary
    :param raise_exception: True to raise an exception, False to send a warnings
    :param chunk: save data every chunk (only if output is not None)
    :return: content of the url

    If the function automatically detects that the downloaded data is in gzip
    format, it will decompress it.

    The function raises the exception @see cl InternetException.
    """

    def save_content(content, append=False):
        "local function"
        app = "a" if append else "w"
        if encoding is not None:
            with open(output, app, encoding=encoding) as f:
                f.write(content)
        else:
            with open(output, app + "b") as f:
                f.write(content)

    try:
        if chunk is not None:
            if output is None:
                raise ValueError("output cannot be None if chunk is not None")
            app = [False]
            size = [0]

            def _local_loop(ur):
                while True:
                    res = ur.read(chunk)
                    size[0] += len(res)  # pylint: disable=E1137
                    if logger.info is not None:
                        logger.info(
                            "[get_url_content_timeout] downloaded %d bytes", size
                        )
                    if len(res) > 0:
                        if encoding is not None:
                            res = res.decode(encoding=encoding)
                        save_content(res, app)
                    else:
                        break
                    app[0] = True  # pylint: disable=E1137

            if timeout != -1:
                with urllib_request.urlopen(url, timeout=timeout) as ur:
                    _local_loop(ur)
            else:
                with urllib_request.urlopen(url) as ur:
                    _local_loop(ur)
            app = app[0]
            size = size[0]
        else:
            if timeout != -1:
                with urllib_request.urlopen(url, timeout=timeout) as ur:
                    res = ur.read()
            else:
                with urllib_request.urlopen(url) as ur:
                    res = ur.read()
    except (
        urllib_error.HTTPError,
        urllib_error.URLError,
        ConnectionRefusedError,
        socket.timeout,
        ConnectionResetError,
        http_client.BadStatusLine,
        http_client.IncompleteRead,
        ValueError,
        InvalidURL,
    ) as e:
        if raise_exception:
            raise InternetException(f"Unable to retrieve content url='{url}'") from e
        warnings.warn(
            f"Unable to retrieve content from '{url}' because of {e}", ResourceWarning
        )
        return None
    except Exception as e:
        if raise_exception:  # pragma: no cover
            raise InternetException(
                f"Unable to retrieve content, url='{url}', exc={e}"
            ) from e
        warnings.warn(
            f"Unable to retrieve content from '{url}' "
            f"because of unknown exception: {e}",
            ResourceWarning,
        )
        raise e

    if chunk is None:
        if len(res) >= 2 and res[:2] == b"\x1f\x8B":
            # gzip format
            res = gzip.decompress(res)

        if encoding is not None:
            try:
                content = res.decode(encoding)
            except UnicodeDecodeError as e:  # pragma: no cover
                # it tries different encoding

                laste = [e]
                othenc = ["iso-8859-1", "latin-1"]

                for encode in othenc:
                    try:
                        content = res.decode(encode)
                        break
                    except UnicodeDecodeError as ee:
                        laste.append(ee)
                        content = None

                if content is None:
                    mes = [f"Unable to parse text from '{url}'."]
                    mes.append("tried:" + str([encoding] + othenc))
                    mes.append("beginning:\n" + str([res])[:50])
                    for e in laste:
                        mes.append("Exception: " + str(e))
                    raise ValueError("\n".join(mes))
        else:
            content = res
    else:
        content = None

    if output is not None and chunk is None:
        save_content(content)

    return content


def download_requirejs(
    to: str = ".",
    location: str = "http://requirejs.org/docs/download.html",
    clean: bool = True,
) -> List[str]:
    """
    Downloads `require.js
    <http://requirejs.org/docs/download.html>`_
    release.

    :param to: where to unzip the files
    :param location: location of require.js release
    :param clean: clean unnecessary files
    :return: list of downloaded and unzipped files

    *require.js* can be locally obtained
    if :epkg:`notebook` is installed.
    """
    if location is None:
        from notebook import __file__ as local_location

        dirname = os.path.dirname(local_location)
        locations = [
            os.path.join(dirname, "static", "components", "requirejs", "require.js"),
            os.path.join(
                dirname,
                "..",
                "nbclassic",
                "static",
                "components",
                "requirejs",
                "require.js",
            ),
            os.path.join(os.path.dirname(__file__), "require.js"),
        ]
        elocations = [loc for loc in locations if os.path.exists(loc)]
        if len(elocations) == 0:
            raise FileNotFoundError(  # pragma: no cover
                f"Unable to find requirejs in '{locations}'"
            )
        location = elocations[0]
        shutil.copy(location, to)
        return [os.path.join(to, "require.js")]
    else:
        link = location
        try:
            page = read_url(link, encoding="utf8")
        except ReadUrlException:  # pragma: no cover
            if logger.info:
                logger.info("[download_requirejs] unable to read %r", location)
            return download_requirejs(to=to, location=None, clean=clean)

        reg = re.compile('href=\\"(.*?minified/require[.]js)\\"')
        alls = reg.findall(page)
        if len(alls) == 0:
            raise RuntimeError(  # pragma: no cover
                f"Unable to find a link on require.js file on page {page!r}."
            )

        filename = alls[0]

        try:
            local = download(filename, to)
        except ReadUrlException as e:  # pragma: no cover
            # We implement a backup plan.
            new_filename = "http://www.xavierdupre.fr/enseignement/setup/require.js/2.3.6/require.js"
            try:
                local = download(new_filename, to)
            except ReadUrlException:
                raise ReadUrlException(
                    "Unable to download '{0}' or '{1}'".format(filename, new_filename)
                ) from e

        logger.info("[download_requirejs] local file %r", local)
        return [local]
