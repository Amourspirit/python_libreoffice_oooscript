# coding: utf-8
from typing import cast
import json
from pathlib import Path
from oooscript.build.embed_py_script import EmbedScriptPy


def test_embed(root_path, fix_my_first_macro_path, clear_build_script) -> None:
    from oooscript.res.docs import __res_path_docs__
    from oooscript.models.example.model_example import ModelExample
    from oooscript.utils import util

    # call get_app_cfg() to set util._APP_CFG global.
    config = util.get_app_cfg()
    macro_config = fix_my_first_macro_path("config.json")
    doc_path = Path(__res_path_docs__, "blank.odt")

    with open(macro_config, "r") as file:
        jdata: dict = json.load(file)

    model = ModelExample(**jdata)
    src = Path(fix_my_first_macro_path("script.py"))
    eb = EmbedScriptPy(src=src, doc_path=doc_path, model=model)
    eb.embed()
    build_path = cast(Path, root_path / config.app_build_dir)

    output = build_path / f"{model.args.output_name}.odt"
    assert output.exists()
