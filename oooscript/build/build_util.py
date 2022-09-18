# coding: utf-8
from pathlib import Path
from ..utils import util


def get_build_path() -> Path:
    """
    Gets path to build directory

    Returns:
        Path: build directory path
    """
    config = util.get_app_cfg()
    build_dir = util.get_path(config.app_build_dir)
    if build_dir.is_absolute():
        return build_dir

    root = Path(util.get_root())
    return root / build_dir
