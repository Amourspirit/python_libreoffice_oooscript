# coding: utf-8

from dataclasses import dataclass
from typing import Any, Dict, List
from dotenv import dotenv_values
from ..res import __res_path__


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
    app_res_dir: str
    """
    Path Like structure to resources dir
    """
    app_res_blank_odt: List[str]
    """
    Path Like structure to resources dir.
    
    This is expected to be a subpath of ``app_res_dir``.
    """
    xml_manifest_namesapce: str
    """
    Name of LO manifest xml file such as `urn:oasis:names:tc:opendocument:xmlns:manifest:1.0`
    """
    build_remove_modules: List[str]
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
        "app_res_dir": __res_path__,
        "app_res_blank_odt": ["odt", "blank.odt"],
        "xml_manifest_namesapce": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
        "build_remove_modules": ["uno", "scriptforge", "access2base"],
        "build_include_paths": ["."],
    }
    return config


def read_config(config_name: str) -> AppConfig:
    """
    Gets config for given config file

    Args:
        config_file (str): Config file to load

    Returns:
        AppConfig: Configuration object
    """
    default_cfg = _get_default_config()
    config = dotenv_values(config_name)
    default_cfg.update(config)
    return AppConfig(**default_cfg)


def read_config_default() -> AppConfig:
    """
    Loads default configuration ``config.json``

    Returns:
        AppConfig: Configuration Object
    """
    return read_config(config_name=".env")
