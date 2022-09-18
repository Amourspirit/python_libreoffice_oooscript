from pathlib import Path

from oooscript.utils import util


def test_build_util_relative(monkeypatch) -> None:
    from oooscript.build import build_util

    # call get_app_cfg() to set util._APP_CFG global.
    _ = util.get_app_cfg()

    monkeypatch.setattr(util._APP_CFG, "app_build_dir", "some_value")
    build_path = build_util.get_build_path()
    assert build_path is not None
    tst_path = Path.cwd() / "some_value"
    assert build_path == tst_path


def test_build_util_absolute(monkeypatch) -> None:
    from oooscript.build import build_util

    # call get_app_cfg() to set util._APP_CFG global.
    _ = util.get_app_cfg()
    tst_path = Path.cwd() / "build_me"
    monkeypatch.setattr(util._APP_CFG, "app_build_dir", str(tst_path))
    build_path = build_util.get_build_path()
    assert build_path == tst_path
