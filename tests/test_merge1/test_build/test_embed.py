# coding: utf-8
from typing import cast
import json
from pathlib import Path
from oooscript.build.embed_py_script import EmbedScriptPy


def test_embed(root_path, fix_my_first_macro_path, clear_build_script) -> None:
    from oooscript.res.docs import __res_path_docs__
    from oooscript.models.script_cfg.model_script_cfg import ModelScriptCfg
    from oooscript.cfg import config

    # call get_app_cfg() to set util._APP_CFG global.
    cfg = config.get_app_cfg()
    macro_config = fix_my_first_macro_path("config.json")
    doc_path = Path(__res_path_docs__, "blank.odt")

    with open(macro_config, "r") as file:
        j_data: dict = json.load(file)

    model = ModelScriptCfg(**j_data)
    src = Path(fix_my_first_macro_path("script.py"))
    eb = EmbedScriptPy(src=src, doc_path=doc_path, model=model)
    eb.embed()
    build_path = cast(Path, root_path / cfg.app_build_dir)

    output = build_path / f"{model.args.output_name}.odt"
    assert output.exists()


def test_embed_build_dir(root_path, fix_my_first_macro_path, tmp_path: Path) -> None:
    # Test that the final output is written to the custom build dir.
    from oooscript.res.docs import __res_path_docs__
    from oooscript.models.script_cfg.model_script_cfg import ModelScriptCfg

    # call get_app_cfg() to set util._APP_CFG global.
    macro_config = fix_my_first_macro_path("config.json")
    doc_path = Path(__res_path_docs__, "blank.odt")

    with open(macro_config, "r") as file:
        j_data: dict = json.load(file)

    model = ModelScriptCfg(**j_data)
    src = Path(fix_my_first_macro_path("script.py"))
    build_dir = tmp_path / "build"
    eb = EmbedScriptPy(src=src, doc_path=doc_path, model=model, build_dir=build_dir)
    eb.embed()

    output = build_dir / f"{model.args.output_name}.odt"
    assert output.exists()
