# coding: utf-8
import pytest
from pathlib import Path
from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs

from tests.fixtures import __test__path__


@pytest.fixture(scope="session")
def fix_suduko_path():
    def get_res(fnm: str):
        return Path(__test__path__, "sudoku", fnm)
        # return Path("tests", "sudoku", fnm)

    return get_res


def test_suduko(fix_suduko_path, clear_build_script):
    from oooscript.res.docs import __res_path_docs__

    macro_config = fix_suduko_path("config.json")
    embeded = fix_suduko_path("calc-sudoku.ods")
    args = BuilderArgs(config_json=macro_config, embed_in_doc=True, embed_doc=embeded)
    builder = Builder(args)
    builder.build()
