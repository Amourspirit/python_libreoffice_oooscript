import pytest
import os
import sys
import subprocess
import stat
import platform
import re


@pytest.fixture(scope="session")
def temporary_script(tmp_path_factory: pytest.TempPathFactory):
    fn = tmp_path_factory.mktemp("script_dir") / "script"

    def _temporary_script(contents):
        with open(fn, "w") as script_file:
            script_file.write(contents)

        st = os.stat(fn)
        fn.chmod(st.st_mode | stat.S_IEXEC)
        return fn

    return _temporary_script


@pytest.fixture(scope="session")
def run_shell_cmd() -> bytes:
    def run_shell(cmd) -> str:
        result = subprocess.check_output(cmd)
        return result

    return run_shell


@pytest.fixture(scope="session")
def get_expected_modules():
    def _get_expected_modules(script_str):
        return set(re.findall(r"__scriptmerge_write_module\('([^']*)\.py'", script_str))

    return _get_expected_modules


@pytest.fixture(scope="session")
def cli_script(root_path):
    return root_path / "oooscript" / "cli" / "main.py"


@pytest.fixture(scope="session")
def get_system_env(is_windows):
    """
    Gets Environment used for subprocess.
    This allows temlates to have access to src directory imports.
    """
    myenv = os.environ.copy()
    pypath = ""
    p_sep = ";" if is_windows else ":"
    for d in sys.path:
        pypath = pypath + d + p_sep
    myenv["PYTHONPATH"] = pypath

    return myenv


@pytest.fixture(scope="session")
def run_cli_cmd(cli_script, get_system_env):
    def run_shell(*args, out_path=None) -> str:
        env = get_system_env
        if out_path:
            # this is use in oooscript/cfg/config.py read_config()
            env["OOOSCRIPT_APP_BUILD_DIR"] = str(out_path)

        cmd_args = [sys.executable, str(cli_script)]
        cmd_args = cmd_args + [*args]
        subprocess.run(cmd_args, env=env)

    return run_shell


@pytest.fixture(scope="session")
def chk_script(get_expected_modules):
    def _chk_script(script_path, expected_mod_count=-1, expected_modules=None):

        if expected_mod_count > -1 or expected_modules:
            with open(script_path, "r") as file:
                result = file.read()
            actual_modules = get_expected_modules(result)
        if expected_mod_count > -1:
            assert len(actual_modules) == expected_mod_count
        if expected_modules:
            assert set(expected_modules) == actual_modules

    return _chk_script


@pytest.fixture(scope="session")
def is_windows():
    return platform.system() == "Windows"
