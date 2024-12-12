from __future__ import annotations
import sys
import traceback
import tempfile
from pathlib import Path
from contextlib import contextmanager

import pythonscript  # type: ignore


class ImportDocPyz:
    def __init__(self, pyz_name: str):
        self._sp = None
        self._sfa = self._get_sfa()
        pv = self._get_script_provider()
        self.module_path = pv.dirBrowseNode.rootUrl
        self.pyz_name = pyz_name
        self.module_name = pyz_name.split(".")[0]
        self.allow_print = False
        if self.allow_print:
            print(f"pyz_name: {self.pyz_name}")
            print(f"module_name: {self.module_name}")

    def _get_script_provider(self):
        """Get the user script provider."""
        if self._sp is None:
            doc = XSCRIPTCONTEXT.getDocument()
            self._sp = pythonscript.PythonScriptProvider(XSCRIPTCONTEXT.ctx, doc)
        return self._sp

    def _get_sfa(self):
        """Get the script file access."""
        # com.sun.star.ucb.SimpleFileAccess
        return XSCRIPTCONTEXT.ctx.ServiceManager.createInstance(
            "com.sun.star.ucb.SimpleFileAccess"
        )

    def _copy_to_temp(self) -> None:
        """Copy the file to a temporary location."""
        try:
            self.key_path.mkdir(exist_ok=True)
            dst_pth = self.import_path
            if dst_pth.exists():
                print("_copy_to_temp: dst_pth exists:", dst_pth)
                return dst_pth

            src_file = f"{self.module_path}/{self.pyz_name}"
            if self.allow_print:
                print("_copy_to_temp: src_file:", src_file)
                print("_copy_to_temp: dst_file:", dst_pth)
            self._sfa.copy(src_file, dst_pth.as_uri())
        except Exception as e:
            print(f"_copy_to_temp() Error: {e}")
            traceback.print_exc()
        return None

    def _get_key(self) -> str:
        # current_date = datetime.now().strftime("%Y-%m-%d")
        # key = hashlib.sha256(current_date.encode()).hexdigest()
        key = f"k_{self.module_name}"
        return key

    def set_pyz(self):
        if self.key_path.exists():
            print("set_pyz() new path exists:", self.key_path)
            return
        self._copy_to_temp()

    @property
    def key_path(self):
        key = self._get_key()
        return Path(tempfile.gettempdir()) / key

    @property
    def import_path(self) -> Path:
        return self.key_path / self.pyz_name


@contextmanager
def importer_file(module_path: Path | str):
    pth = str(Path(module_path))
    sys.path.insert(0, pth)
    try:
        yield
    finally:
        sys.path.remove(pth)


try:
    ipd = ImportDocPyz("___pyz___.pyz")
    ipd.set_pyz()
    if ipd.allow_print:
        print(f"Import Path: {ipd.import_path}")
    with importer_file(ipd.import_path):
___code_placeholder___

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
