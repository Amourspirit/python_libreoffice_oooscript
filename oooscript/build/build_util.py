# coding: utf-8
from pathlib import Path
from ..utils import paths
from ..cfg import config


def get_build_path() -> Path:
    """
    Gets path to build directory

    Returns:
        Path: build directory path
    """
    cfg = config.get_app_cfg()
    build_dir = paths.get_path(cfg.app_build_dir)
    if build_dir.is_absolute():
        return build_dir

    root = Path(paths.get_root())
    return root / build_dir
