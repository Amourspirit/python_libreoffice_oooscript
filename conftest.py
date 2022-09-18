# coding: utf-8
import pytest
from pathlib import Path
from tests.fixtures.my_first_macro import __test__path__ as test_my_first_macro_path

@pytest.fixture(scope="session")
def root_path():
    return Path(__file__).parent