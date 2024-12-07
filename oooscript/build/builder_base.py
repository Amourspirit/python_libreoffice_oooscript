from __future__ import annotations
import os
import sys
from abc import ABC
from pathlib import Path


class BuilderBase(ABC):
    def __init__(self) -> None:
        self._site_pkg_dir = None

    def _get_virtual_env_path(self) -> str:
        """
        Gets the Virtual Environment Path such as `'/tmp/ds/.venv'`

        Returns:
            str: Virtual Environment Path
        """
        s_path = os.environ.get("VIRTUAL_ENV", None)
        if s_path is not None:
            return s_path
        raise FileNotFoundError("Unable to get Virtual Environment Path")

    def _get_virtual_site_pkg_dir(self) -> str:
        """
        Gets the Virtual Site Package Directory such as `'/tmp/ds/.venv/lib/python3.8/site-packages'`

        Returns:
            str: Virtual Site Package Directory
        """
        env_path = Path(self._get_virtual_env_path())
        major, minor, *_ = sys.version_info
        site_packages_path = (
            env_path / "lib" / f"python{major}.{minor}" / "site-packages"
        )
        if not site_packages_path.exists():
            # windows
            site_packages_path = env_path / "Lib" / "site-packages"
        if not site_packages_path.exists():
            raise FileNotFoundError("Unable to get Site Packages Path")
        return str(site_packages_path)

    @property
    def site_pkg_dir(self):
        if self._site_pkg_dir is None:
            self._site_pkg_dir = self._get_virtual_site_pkg_dir()
        return self._site_pkg_dir
