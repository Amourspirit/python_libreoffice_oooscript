# coding: utf-8
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List
from dotenv import dotenv_values
from ..res import __res_path__
from ..utils import paths


_APP_CFG = None
@dataclass
class AppConfig:

    lo_script_dir: str
    """
    Path Like structure to libre office scripts director.
    """
    app_build_dir: str
    """
    Path Like structure to build dir
    """
    xml_manifest_namespace: str
    """
    Name of LO manifest xml file such as `urn:oasis:names:tc:opendocument:xmlns:manifest:1.0`
    """
    build_exclude_modules: List[str]
    """
    Modules to remove from compiled scripts such as ['uno', 'scriptforge', 'access2base']
    
    This list is combined with an examples config.json remove_modules property
    """
    build_include_paths: List[str]
    """
    Module include paths that is used to find module that may be included in compiled scripts such as ['.']
    
    This list is combined with an examples config.json include_paths property
    """


def _get_default_config() -> Dict[str, Any]:
    config = {
        "lo_script_dir": "~/.config/libreoffice/4/user",
        "app_build_dir": "build_script",
        "xml_manifest_namespace": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
        "build_exclude_modules": ["uno\\.*", "unohelper\\.*", "scriptforge\\.*", "access2base\\.*"],
        "build_include_paths": ["."],
    }
    return config

def _split_list(cfg:Dict[str, str]) -> None:
    args = ("build_exclude_modules", "build_include_paths")
    for arg in args:
        value = cfg.get(arg, None)
        if value is not None:
            if value == "":
                cfg[arg] = []
            else:
                sl = value.split(',')
                cfg[arg] = [s.strip() for s in sl]
    

def read_config(config_name: str) -> AppConfig:
    """
    Gets config for given config file

    Args:
        config_file (str): Config file to load

    Returns:
        AppConfig: Configuration object
    """
    default_cfg = _get_default_config()
    try:
        config = dotenv_values(config_name)
        _split_list(config)
        default_cfg.update(config)
    except Exception:
        pass
    # can override app build directory from environment.
    # this is for testing purposes
    app_build = os.environ.get("OOOSCRIPT_APP_BUILD_DIR", None)
    if app_build:
        default_cfg["app_build_dir"] = app_build
    return AppConfig(**default_cfg)


def read_config_default() -> AppConfig:
    """
    Loads default configuration ``config.json``

    Returns:
        AppConfig: Configuration Object
    """
    return read_config(config_name=".env")


def get_app_cfg() -> AppConfig:
    """
    Get App Config. config is cached
    """
    global _APP_CFG
    if _APP_CFG is None:
        _APP_CFG = read_config_default()
    return _APP_CFG