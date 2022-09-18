from oooscript.utils import paths
from pathlib import Path
from oooscript.cfg import config

def test_root_path() -> None:
    root = paths.get_root()
    assert root != ""
    p_root = Path(root)
    assert p_root.exists()
    assert p_root.is_dir()

def test_get_app_config() -> None:
    cfg = config.get_app_cfg()
    assert cfg is not None
