from oooscript.utils import util
from pathlib import Path

def test_root_path() -> None:
    root = util.get_root()
    assert root != ""
    p_root = Path(root)
    assert p_root.exists()
    assert p_root.is_dir()

def test_get_app_config() -> None:
    config = util.get_app_cfg()
    assert config is not None
