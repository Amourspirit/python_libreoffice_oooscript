# coding: utf-8
import pytest
from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs


def test_suduko(fix_suduko_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_suduko_path("config.json")
    embedded = fix_suduko_path("calc-sudoku.ods")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=embedded)
    builder = Builder(args)
    builder.build()
