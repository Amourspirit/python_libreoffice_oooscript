# coding: utf-8
from __future__ import annotations
import os
import sys
import shutil
import __main__
from pathlib import Path
from typing import Iterator, List, Union, overload
from dotenv.main import find_dotenv

_APP_ROOT = None
_OS_PATH_SET = False
_PKG_ROOT = None


def get_uno_path() -> Path:
    """
    Searches known paths for path that contains uno.py

    This path is different for windows and linux.
    Typically for Windows ``C:\Program Files\LibreOffice\program``
    Typically for Linux ``/usr/lib/python3/dist-packages``

    Raises:
        FileNotFoundError: if path is not found
        NotADirectoryError: if path is not a directory

    Returns:
        Path: First found path.
    """
    if os.name == "nt":

        p_uno = Path(os.environ["PROGRAMFILES"], "LibreOffice", "program")
        if p_uno.exists() is False or p_uno.is_dir() is False:
            p_uno = Path(os.environ["PROGRAMFILES(X86)"], "LibreOffice", "program")
        if not p_uno.exists():
            raise FileNotFoundError("Uno Source Dir not found.")
        if not p_uno.is_dir():
            raise NotADirectoryError("UNO source is not a Directory")
        return p_uno
    else:
        p_uno = Path("/usr/lib/python3/dist-packages")
        if not p_uno.exists():
            raise FileNotFoundError("Uno Source Dir not found.")
        if not p_uno.is_dir():
            raise NotADirectoryError("UNO source is not a Directory")
        return p_uno


def get_lo_path() -> Path:
    """
    Searches known paths for path that contains LibreOffice ``soffice``.

    This path is different for windows and linux.
    Typically for Windows ``C:\Program Files\LibreOffice\program``
    Typically for Linux `/usr/bin/soffice``

    Raises:
        FileNotFoundError: if path is not found
        NotADirectoryError: if path is not a directory

    Returns:
        Path: First found path.
    """
    if os.name == "nt":

        p_uno = Path(os.environ["PROGRAMFILES"], "LibreOffice", "program")
        if p_uno.exists() is False or p_uno.is_dir() is False:
            p_uno = Path(os.environ["PROGRAMFILES(X86)"], "LibreOffice", "program")
        if not p_uno.exists():
            raise FileNotFoundError("LibreOffice Source Dir not found.")
        if not p_uno.is_dir():
            raise NotADirectoryError("LibreOffice source is not a Directory")
        return p_uno
    else:
        # search system path
        s = shutil.which("soffice")
        p_sf = None
        if s is not None:
            # expect '/usr/bin/soffice'
            if os.path.islink(s):
                p_sf = Path(os.path.realpath(s)).parent
            else:
                p_sf = Path(s).parent
        if p_sf is None:
            p_sf = Path("/usr/bin/soffice")
        if not p_sf.exists():
            raise FileNotFoundError("LibreOffice Source Dir not found.")
        if not p_sf.is_dir():
            raise NotADirectoryError("LibreOffice source is not a Directory")
        return p_sf


def get_lo_python_ex() -> str:
    """
    Gets the python executable for different environments.

    In Linux this is the current python executable.
    If a virtual environment is activated then that will be the
    python exceutable that is returned.

    In Windows this is the python.exe file in LibreOffice.
    Typically for Windows ``C:\Program Files\LibreOffice\program\python.exe``

    Raises:
        FileNotFoundError: In Windows if python.exe is not found.
        NotADirectoryError: In Windows if python.exe is not a file.

    Returns:
        str: file location of python executable.
    """
    if os.name == "nt":
        p = Path(get_lo_path(), "python.exe")

        if not p.exists():
            raise FileNotFoundError("LibreOffice python executable not found.")
        if not p.is_file():
            raise NotADirectoryError("LibreOffice  python executable is not a file")
        return str(p)
    else:
        return sys.executable


def get_root() -> str:
    """
    Gets Application Root Path

    Returns:
        str: App root as string.
    """
    global _APP_ROOT
    if _APP_ROOT is None:
        try:
            root = find_dotenv(raise_error_if_not_found=True)
        except IOError:
            _APP_ROOT = os.getcwd()
            return _APP_ROOT

        if root == "":
            root = os.environ.get("project_root", "")
        else:
            root = str(Path(root).parent)  # drop .env

        if root == "":
            raise Exception("Unable to find Project root dir. Make sure .env file exists.")
        _APP_ROOT = root
    return _APP_ROOT


def set_os_root_path() -> None:
    """
    Ensures application root dir is in sys.path
    """
    global _OS_PATH_SET
    if _OS_PATH_SET is False:
        _app_root = get_root()
        if not _app_root in sys.path:
            sys.path.insert(0, _app_root)
    _OS_PATH_SET = True


def _walk_to_root(path: str) -> Iterator[str]:
    """
    Yield directories starting from the given directory up to the root
    """
    if not os.path.exists(path):
        raise IOError("Starting path not found")

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_higher_file(
    filename: str = ".oooscript_root",
    raise_error_if_not_found: bool = False,
    usecwd: bool = False,
) -> Path | None:
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or None otherwise
    """

    def _is_interactive():
        """Decide whether this is running in a REPL or IPython notebook"""
        main = __import__("__main__", None, None, fromlist=["__file__"])
        return not hasattr(main, "__file__")

    if usecwd or _is_interactive() or getattr(sys, "frozen", False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path = os.getcwd()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_code.co_filename == current_file:
            assert frame.f_back is not None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return Path(check_path)

    if raise_error_if_not_found:
        raise IOError("File not found")

    return None


def get_pkg_root() -> Path:
    """
    Gets the Root directory of oooscript.

    Path is cached.

    Raises:
        IOError: If unable to get root directory

    Returns:
        str: Package root as string path.
    """
    global _PKG_ROOT
    if _PKG_ROOT is not None:
        return _PKG_ROOT
    root = find_higher_file()
    if root is None:
        raise IOError("Unable to find root directory of oooscript")
    _PKG_ROOT = root.parent
    return _PKG_ROOT


@overload
def get_path(path: str, ensure_absolute: bool = False) -> Path:
    ...


@overload
def get_path(path: List[str], ensure_absolute: bool = False) -> Path:
    ...


@overload
def get_path(path: Path, ensure_absolute: bool = False) -> Path:
    ...


def get_path(path: Union[str, Path, List[str]], ensure_absolute: bool = False) -> Path:
    """
    Builds a Path from a list of strings

    If path starts with ``~`` then it is expanded to user home dir.

    Args:
        lst (List[str], Path, str): List of path parts
        ensure_absolute (bool, optional): If true returned will have root dir prepended
            if path is not absolute

    Raises:
        ValueError: If lst is empty

    Returns:
        Path: Path of combined from ``lst``
    """
    p = None
    lst = []
    expand = None
    if isinstance(path, str):
        expand = path.startswith("~")
        p = Path(path)
    elif isinstance(path, Path):
        p = path
    else:
        lst = [s for s in path]
    if p is None:
        if len(lst) == 0:
            raise ValueError("lst arg is zero length")
        arg = lst[0]
        expand = arg.startswith("~")
        p = Path(*lst)
    else:
        if expand is None:
            pstr = str(p)
            expand = pstr.startswith("~")
    if expand:
        p = p.expanduser()
    if ensure_absolute is True and p.is_absolute() is False:
        p = Path(get_root(), p)
    return p


@overload
def mkdirp(dest_dir: str) -> None:
    ...


@overload
def mkdirp(dest_dir: Path) -> None:
    ...


def mkdirp(dest_dir: Union[str, Path]) -> None:
    """
    Creates path and subpaths not existing.

    Args:
        dest_dir (Union[str, Path]): PathLike object

    Since:
        Python 3.5
    """
    # Python ≥ 3.5
    if isinstance(dest_dir, Path):
        dest_dir.mkdir(parents=True, exist_ok=True)
    else:
        Path(dest_dir).mkdir(parents=True, exist_ok=True)


def _get_virtual_path() -> str:
    spath = os.environ.get("VIRTUAL_ENV", None)
    if spath is not None:
        return spath
    return sys.base_exec_prefix


def get_site_packeges_dir() -> Union[Path, None]:
    """
    Gets the ``site-packages`` directory for current python environment.

    Returns:
        Union[Path, None]: site-packages dir if found; Otherwise, None.
    """
    v_path = _get_virtual_path()
    p_site = Path(v_path, "Lib", "site-packages")
    if p_site.exists() and p_site.is_dir():
        return p_site

    ver = f"{sys.version_info[0]}.{sys.version_info[1]}"
    p_site = Path(v_path, "lib", f"python{ver}", "site-packages")
    if p_site.exists() and p_site.is_dir():
        return p_site
    return None

def get_pkg_res_path() -> Path:
    """
    Gets oooscript's ressource path

    Returns:
        Path: Resource Path
    """
    root = get_pkg_root()
    return root / "res"