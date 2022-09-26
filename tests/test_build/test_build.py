# coding: utf-8
from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs


def test_first_macro_write(fix_my_first_macro_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_my_first_macro_path("config.json")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True)
    builder = Builder(args)
    builder.build()


def test_msgbox_writer(fix_msgbox_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = fix_msgbox_path("msgbox.odt")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    builder.build()


def test_msgbox_calc(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.ods"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    builder.build()


def test_msgbox_presentation(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.odp"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    builder.build()


def test_msgbox_math(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.odf"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    builder.build()


def test_msgbox_drawing(fix_msgbox_path, res_docs_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_msgbox_path("config.json")
    embed_doc = res_docs_path / "blank.odg"
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=str(embed_doc))
    builder = Builder(args)
    builder.build()
