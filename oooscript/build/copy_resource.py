# coding: utf-8
from __future__ import annotations
import os
import shutil
from pathlib import Path
from typing import Union, List
from ..utils import paths
from ..cfg import config


class CopyResource:
    """
    Copies a resource from the source or into destination dir.
    Resource can be a file or a dir.
    """

    def __init__(
        self,
        src: str | Path | List[str],
        dst: str | Path | List[str] | None,
        dst_is_file: bool = False,
        clear_prev: bool = True,
        src_is_res: bool = True
    ) -> None:
        """
        Constructor

        Arguments:
            src (str | Path | List[str]): path to the resource to copy. This can be a path to a file or dir.
            dst (str | Path | List[str]): destination path to copy resource.
            dst_is_file (bool, optional): Specifies if ``dst`` is a file or a dir. Default ``False``
            clear_previous (bool, optional): If ``True`` previous files/dir will be cleared before resources are copied. Default: ``True``
            src_is_res (bool, Optional): Specifies if ``src`` is in the resource. Default ``True``
            config (AppConfig, Optional): App config. Default ``None``
        Raises:
            FileNotFoundError: If resource path is not found.
        """
        self._config = config.get_app_cfg()
        self._clear_previous = clear_prev
        _src = paths.get_path(src)
        self._dst_is_file = dst_is_file
        if dst is None:
            _dst = None
        else:
            _dst = paths.get_path(dst, ensure_absolute=True)

        if src_is_res:
            if _src.is_absolute():
                self._src = _src
            else:
                res_path = paths.get_pkg_res_path()
                self._src = Path(res_path, _src)
        else:
            self._src = paths.get_path(_src, ensure_absolute=True)
        if not self._src.exists():
            raise FileNotFoundError(f"{self.__class__.__name__} unable to find resource path: '{self._src}'")
        if _dst is None:
            self._dst = None
        else:
            if self._dst_is_file:
                self._dst = _dst
            else:
                self._dst = Path(_dst, self._src.name)

    def copy(self) -> None:
        """
        Copies source to dest.
        """
        if self._dst is None:
            raise ValueError("Destination not set")
        if self._src.is_dir():
            self._copy_dir()
        elif self._src.is_file():
            self._copy_file()

    def _copy_dir(self) -> None:
        if self._clear_previous == True and self._dst.exists():
            shutil.rmtree(self._dst)
        paths.mkdirp(self._dst)
        shutil.copytree(str(self._src), str(self._dst))

    def _copy_file(self) -> None:
        p_dir = self._dst.parent
        paths.mkdirp(p_dir)
        self._remove_files_in_dir(p_dir)
        shutil.copy2(self._src, self._dst)

    def _remove_files_in_dir(self, src_dir: Path) -> None:
        if self._clear_previous == False:
            return None
        if src_dir.exists() is False:
            return None
        for f in os.listdir(src_dir):
            f_path = Path(src_dir, f)
            if f_path.is_file():
                os.remove(f_path)

    @property
    def dst_path(self) -> Union[Path, None]:
        """
        Gets the path to the dest directory/file.
        """
        return self._dst

    @property
    def src_path(self) -> Path:
        """
        Gets the path to the dest directory/file.
        """
        return self._src

    @property
    def clear_previous(self) -> bool:
        """Gets if the previous files will be cleared"""
        return self._clear_previous
