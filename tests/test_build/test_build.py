# coding: utf-8
from pathlib import Path
from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs

def test_first_macro(fix_my_first_macro_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__
    macro_config = fix_my_first_macro_path("config.json")
    doc_path = Path(__res_path_docs__, "blank.odt")
    args = BuilderArgs(
        config_json=macro_config,
        embed_in_doc=True
        )
    builder = Builder(args)
    builder.build()