import pytest
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from oooscript.models.script_cfg.model_script_cfg import ModelScriptCfg


@pytest.mark.parametrize(
    "fix_macro_path, expected_mod_count, expected_modules, ext",
    [
        ("fix_my_first_macro_path", 0, None, "odt"),
        ("fix_msgbox_path", 1623, None, "odt"),
        ("fix_suduko_path", 14, None, "ods"),
    ],
)
def test_writes_py(
    fix_macro_path,
    expected_mod_count: int,
    expected_modules: list,
    ext: str,
    run_cli_cmd,
    tmp_path: Path,
    get_config_model,
    unzip,
    chk_script,
    request,
) -> None:
    from oooscript.res.docs import __res_path_docs__
    from oooscript.build.manifest_script import ManifestScript

    fix_my_first_macro_path = request.getfixturevalue(fix_macro_path)

    macro_config = fix_my_first_macro_path("config.json")
    model = cast("ModelScriptCfg", get_config_model(macro_config))
    run_cli_cmd("compile", "--embed", "--config", str(macro_config), out_path=tmp_path)
    out_file = tmp_path / f"{model.args.output_name}.py"
    out_doc = tmp_path / f"{model.args.output_name}.{ext}"

    assert out_file.exists()

    zip_extract_dst = Path(tmp_path, "extracted")
    unzip(source=out_doc, dest=zip_extract_dst)
    assert zip_extract_dst.exists()
    manifest_file = zip_extract_dst / "META-INF" / "manifest.xml"
    assert manifest_file.exists()
    ms = ManifestScript(
        manifest_path=manifest_file, script_name=f"{model.args.output_name}.py"
    )
    assert ms.verify(ms.read())

    script_path = (
        zip_extract_dst / "Scripts" / "python" / f"{model.args.output_name}.py"
    )
    assert script_path.exists()
    chk_script(
        script_path=script_path,
        expected_mod_count=expected_mod_count,
        expected_modules=expected_modules,
    )


@pytest.mark.parametrize(
    "fix_macro_path, ext",
    [
        ("fix_my_first_macro_path", "odt"),
        ("fix_msgbox_path", "odt"),
        ("fix_suduko_path", "ods"),
    ],
)
def test_writes_py_custom_build_dir(
    fix_macro_path,
    ext: str,
    run_cli_cmd,
    tmp_path: Path,
    get_config_model,
    unzip,
    chk_script,
    request,
) -> None:
    # test the the build dir is overridden by command line --build-dir option.
    from oooscript.res.docs import __res_path_docs__

    build_path = tmp_path / "build"

    fix_my_first_macro_path = request.getfixturevalue(fix_macro_path)

    macro_config = fix_my_first_macro_path("config.json")
    model = cast("ModelScriptCfg", get_config_model(macro_config))
    run_cli_cmd(
        "compile",
        "--embed",
        "--config",
        str(macro_config),
        "--build-dir",
        str(build_path),
        out_path=None,
    )
    out_file = build_path / f"{model.args.output_name}.py"

    assert out_file.exists()
