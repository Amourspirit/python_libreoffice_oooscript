from __future__ import annotations
from pathlib import Path
from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs


def test_first_macro_write(fix_my_first_macro_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_my_first_macro_path("config.json")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True)
    builder = Builder(args)
    assert builder.build()


def test_msgbox_writer(fix_msgbox_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = fix_msgbox_path("msgbox.odt")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    assert builder.build()


def test_msgbox_calc(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.ods"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    assert builder.build()


def test_msgbox_calc_blank(fix_msgbox_path, clear_build_script, monkeypatch):
    from oooscript.lib.enums import AppTypeEnum

    macro_config = fix_msgbox_path("config.json")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True)
    builder = Builder(args)
    monkeypatch.setattr(builder._model, "app", AppTypeEnum.CALC)
    assert builder.build()


def test_msgbox_presentation(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.odp"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    assert builder.build()


def test_msgbox_presentation_blank(fix_msgbox_path, clear_build_script, monkeypatch):
    from oooscript.lib.enums import AppTypeEnum

    macro_config = fix_msgbox_path("config.json")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True)
    builder = Builder(args)
    monkeypatch.setattr(builder._model, "app", AppTypeEnum.IMPRESS)
    assert builder.build()


def test_msgbox_math(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.odf"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    assert builder.build()


def test_msgbox_drawing(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.odg"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    assert builder.build()


def test_builder_build_dir(fix_my_first_macro_path, tmp_path: Path, clear_build_script):
    # override the build dir and make sure the file is written to the correct location.
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_my_first_macro_path("config.json")
    build_path = tmp_path / "build"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, build_dir=build_path)
    builder = Builder(args)
    assert builder.build()
    out_file = build_path / "my_first_macro.py"
    assert out_file.exists()
