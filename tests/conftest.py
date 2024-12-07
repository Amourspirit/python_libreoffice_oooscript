# coding: utf-8
import pytest
import json
from pathlib import Path
import zipfile

from tests.fixtures.msg_box import __test__path__ as test_msgbox_path
from tests.fixtures.sudoku import __test__path__ as test_sudoku_path
from tests.fixtures.my_first_macro import __test__path__ as test_my_first_macro_path
from tests.fixtures.xml import __test__path__ as test_xml_path


@pytest.fixture(scope="session")
def res_path(root_path):
    return root_path / "oooscript" / "res"


@pytest.fixture(scope="session")
def res_path():
    return Path(__file__).parent.parent / "oooscript" / "res"


@pytest.fixture(scope="session")
def res_docs_path(res_path):
    return res_path / "docs"


@pytest.fixture(scope="session")
def fix_my_first_macro_path():
    def get_res(fnm: str):
        return Path(test_my_first_macro_path, fnm)

    return get_res


@pytest.fixture(scope="session")
def fix_xml_path_path():
    def get_res(fnm: str):
        return Path(test_xml_path, fnm)

    return get_res


@pytest.fixture(scope="session")
def fix_msgbox_path():
    def get_res(fnm: str):
        return Path(test_msgbox_path, fnm)

    return get_res


@pytest.fixture(scope="session")
def fix_suduko_path(res_docs_path):
    def get_res(fnm: str):
        return Path(test_sudoku_path, fnm)
        # return Path("tests", "sudoku", fnm)

    return get_res


@pytest.fixture(scope="session")
def get_config_model():
    from oooscript.models.script_cfg.model_script_cfg import ModelScriptCfg

    def _get_config_model(config_path) -> ModelScriptCfg:
        with open(config_path, "r") as file:
            data = json.load(file)
        return ModelScriptCfg(**data)

    return _get_config_model


@pytest.fixture(scope="session")
def unzip() -> None:
    def _unzip(source: Path, dest: Path) -> None:
        with zipfile.ZipFile(str(source), "r") as zip_ref:
            zip_ref.extractall(str(dest))

    return _unzip
