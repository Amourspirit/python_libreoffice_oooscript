# coding: utf-8
import pytest
from pathlib import Path
import shutil
from tests.fixtures.my_first_macro import __test__path__ as test_my_first_macro_path
from tests.fixtures.msg_box import __test__path__ as test_msgbox_path


BUILD_PATH = "build_script"

@pytest.fixture(scope="session")
def res_path():
    return Path(__file__).parent.parent / "oooscript" / "res"
    # /media/data_main/Users/bigby/Projects/python/linux/oooscript/oooscript/res/docs

@pytest.fixture(scope="session")
def res_docs_path(res_path):
    return res_path / "docs"

@pytest.fixture(scope="session")
def fix_my_first_macro_path():
    def get_res(fnm: str):
        return Path(test_my_first_macro_path, fnm)

    return get_res

@pytest.fixture(scope="session")
def fix_msgbox_path():
    def get_res(fnm: str):
        return Path(test_msgbox_path, fnm)

    return get_res

@pytest.fixture(scope="session")
def clear_build_script(root_path):
    p = root_path / BUILD_PATH
    shutil.rmtree(str(p), ignore_errors=True)