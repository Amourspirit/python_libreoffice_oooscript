# coding: utf-8
import pytest
import shutil


@pytest.fixture(scope="session")
def clear_build_script(root_path):
    p = root_path / "build_script2"
    shutil.rmtree(str(p), ignore_errors=True)
