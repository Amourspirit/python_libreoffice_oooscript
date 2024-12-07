from __future__ import annotations
import sys
import re
import traceback
import shutil
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

    def _copy_to_temp(self, filename: str) -> Path | None:
        """Copy the file to a temporary location."""
        try:
            tmp_dir = Path(tempfile.gettempdir()) / filename.replace(".", "_")
            tmp_dir.mkdir(exist_ok=True)
            dst_pth = tmp_dir / filename
            if dst_pth.exists():
                print("_copy_to_temp: dst_pth exists:", dst_pth)
                return dst_pth

            src_file = f"{self.module_path}/{filename}"
            if self.allow_print:
                print("_copy_to_temp: src_file:", src_file)
                print("_copy_to_temp: dst_file:", dst_pth)
            self._sfa.copy(src_file, dst_pth.as_uri())
            return dst_pth
        except Exception as e:
            print(f"_copy_to_temp() Error: {e}")
            traceback.print_exc()
        return None

    def _convert_to_relative_imports(self, file_path: Path):
        # the __main__.py file must convert absolute imports to relative imports because is is a top level module.
        # Top level modules must use relative or absolute imports to import other modules in the same package.
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Regular expression to match absolute imports
        import_pattern = re.compile(r"^(import|from) (\w+)", re.MULTILINE)

        # Function to replace absolute imports with relative imports
        def replace_import(match):
            import_type, module_name = match.groups()
            return f"{import_type} .{module_name}"

        # Replace all absolute imports with relative imports
        new_content = import_pattern.sub(replace_import, content)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

    def _extract_pyz(self, zip_pth: Path) -> Path | None:
        """Extract the pyz file."""

        try:
            dst_pth = self.extracted_path / self.module_name
            dst_pth.mkdir(exist_ok=True, parents=True)
            # dst_pth = tmp_dir / self.module_name
            main_pth = dst_pth / "__main__.py"
            if main_pth.exists():
                if self.allow_print:
                    print("_extract_pyz: dst_pth exists:", dst_pth)
                return dst_pth.parent

            shutil.unpack_archive(zip_pth, dst_pth, "zip")
            zip_pth.unlink()
            zip_pth.parent.rmdir()
            if main_pth.exists():
                self._convert_to_relative_imports(main_pth)
            return dst_pth.parent
        except Exception as e:
            print(f"_extract_pyz() Error: {e}")
            traceback.print_exc()
        return None

    def _get_key(self) -> str:
        # current_date = datetime.now().strftime("%Y-%m-%d")
        # key = hashlib.sha256(current_date.encode()).hexdigest()
        key = f"k_{self.module_name}"
        return key

    def set_pyz(self):
        key = self._get_key()
        extracted_pth = Path(tempfile.gettempdir()) / key
        if extracted_pth.exists():
            print("set_pyz() extracted_pth exists:", extracted_pth)
            # self._add_to_sys_path(str(extracted_pth))
            return
        zip_pth = self._copy_to_temp(self.pyz_name)
        if zip_pth:
            _ = self._extract_pyz(zip_pth)
            pth = self.extracted_path
            if pth:
                sys_pth = str(pth)
                if self.allow_print:
                    print(f"set_pyz() set_pyz for: {sys_pth}")
                # self._add_to_sys_path(sys_pth)
            else:
                if self.allow_print:
                    print(f"set_pyz() Error: Could not set_pyz for: {self.pyz_name}")
        else:
            if self.allow_print:
                print(f"set_pyz() Error: Could not set_pyz for: {self.pyz_name}")

    @property
    def extracted_path(self):
        key = self._get_key()
        return Path(tempfile.gettempdir()) / key


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
        print(f"extracted_path: {ipd.extracted_path}")
    with importer_file(ipd.extracted_path):
        from ___pyz___.__main__ import *
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
