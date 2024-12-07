# coding: utf-8
from __future__ import annotations
from typing import Tuple
import json
from pathlib import Path
import os
from dataclasses import dataclass
from typing import List, Optional, Union
import uuid
import scriptmerge

from .embed_py_script import EmbedScriptPy
from .copy_resource import CopyResource
from ..utils import paths
from ..cfg import config
from ..models.script_cfg.model_script_cfg import ModelScriptCfg
from ..lib.enums import AppTypeEnum
from .builder_base import BuilderBase
from ..res.code import __res_path__ as code_res_path


@dataclass
class BuilderArgs:
    config_json: str | Path
    """
    Path to json file that contains configuration
    """
    allow_print: bool = False
    """
    If True some print statements will be made in the terminal
    """
    embed_in_doc: bool = False
    """
    If True then an odt file with embedded script is generated
    """
    pyz_out: bool = False
    """
    If True then a pyz file is generated
    """
    embed_doc: Optional[str] = None
    """
    The document to embed compile script into.
    
    Requires ``embed_in_doc`` be ``True``.
    
    If ``embed_in_doc`` be ``True`` then the default used document to embed
    is internal .odt file.
    """
    build_dir: Union[str, Path, None] = None
    """
    Build directory to place compiled script. Will override the build directory set by environment and config.json.
    """


class Builder2(BuilderBase):
    """Builder Class"""

    # region Constructor
    def __init__(self, args: BuilderArgs):
        """
        Constructor

        Arguments:
            args (BuilderArgs): Builder Args
        """
        super().__init__()
        self._config = config.get_app_cfg()
        self._allow_print = args.allow_print
        self._embed = args.embed_in_doc
        self._embed_doc = args.embed_doc
        self._builder_args = args
        self._dest_file = ""
        self._prelude_file = ""
        self._json_cfg = paths.get_path(path=args.config_json, ensure_absolute=True)
        # self._json_cfg = paths.get_path_from_lst(
        #     "src/examples/message_box/config.json".split("/"), ensure_absolute=True
        # )
        self._src_path = self._json_cfg.parent
        j_data = json.loads(self._json_cfg.read_text())
        self._model = ModelScriptCfg(**j_data)
        self._src_file = self._get_src_file()
        self._res_path = paths.get_pkg_res_path()

    # endregion Constructor

    def _get_src_file(self) -> Path:
        parts = self._model.args.src_file.replace("\\", "/").split("/")
        rel = paths.get_path(parts, ensure_absolute=False)
        if rel.is_absolute():
            return rel
        return Path(self._src_path, rel)

    def _get_python_modules(self, add_flag="--add-python-module") -> str:
        if len(self._model.args.include_modules) == 0:
            return ""
        result = ""
        for val in self._model.args.include_modules:
            result = result + f" {add_flag} {val}"
        return result

    def _get_include_paths(self) -> List[str]:
        paths = self._config.build_include_paths + self._model.args.include_paths
        paths.append(self.site_pkg_dir)
        # ensure unique values in path.
        return list(set(paths))

    def _get_site_include_path(self) -> str:
        paths = self._get_include_paths()
        result = ""
        for i, p in enumerate(paths):
            if i > 0:
                result = result + " "
            result = f"{result}--add-python-path {p!r}"
        return result

    def _get_g_exported(self) -> str:
        # g_exportedScripts = (
        #     main,
        # )
        count = len(self._model.methods)
        result = "\ng_exportedScripts = ("
        if count > 0:
            body = ",".join(self._model.methods)
            result += body
        if count == 1:
            result += ","
        result += ")\n"
        return result

    def _append_g_exported(self, file_path: str) -> None:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(self._get_g_exported())

    def _get_blank_embed_doc(self) -> Path | None:
        t = self._model.app
        if t == AppTypeEnum.CALC:
            return self._res_path / "docs" / "blank.ods"
        elif t == AppTypeEnum.DRAW:
            return self._res_path / "docs" / "blank.odg"
        elif t == AppTypeEnum.IMPRESS:
            return self._res_path / "docs" / "blank.odp"
        elif t == AppTypeEnum.MATH:
            return self._res_path / "docs" / "blank.odf"
        elif t == AppTypeEnum.WRITER:
            return self._res_path / "docs" / "blank.odt"
        else:
            # base is not currently supported
            return None

    def _embed_scripts(self, build_dir: Path) -> None:
        if self._embed_doc is None:
            # src_doc = self._config.app_res_blank_odt
            src_doc = self._get_blank_embed_doc()
            if src_doc is None:
                return None
        else:
            src_doc = paths.get_path(self._embed_doc)
        cp = CopyResource(
            src=src_doc, dst=None, clear_prev=False, src_is_res=self._embed_doc is None
        )
        embed_sources = [self._dest_file]
        if self._prelude_file:
            embed_sources.append(self._prelude_file)
        emb = EmbedScriptPy(
            src=embed_sources,
            doc_path=cp.src_path,
            model=self._model,
            build_dir=build_dir,
        )
        emb.embed()

    def _get_code_prelude(self, pyz_mod_name: str) -> str:
        with open(
            Path(code_res_path) / "prelude_pyz.py", "r", encoding="utf-8"
        ) as file:
            result: str = file.read()
        return result.replace("___pyz___", pyz_mod_name)

    def _write_prelude_file(self, dist_dir: Path, pyz_mod_name: str) -> Path:
        dest_file = dist_dir / f"{self._model.args.output_name}.py"
        if dest_file.exists():
            dest_file.unlink()
        dest_file.write_text(self._get_code_prelude(pyz_mod_name=pyz_mod_name))
        return str(dest_file)

    # region Public Methods
    def build(self) -> bool:
        """
        Builds the plugin into the dist folder outlined in settings.json
        @return: `True` of the build is a success; Otherwise, `False`
        """
        self._prelude_file = ""
        self._dest_file = ""

        if self._builder_args.pyz_out:
            if self._model.args.single_script:
                raise ValueError("Cannot use pyz_out with single_script")

        if self._builder_args.build_dir is None:
            dist_dir = paths.get_path(self._config.app_build_dir, ensure_absolute=True)
        else:
            dist_dir = paths.get_path(
                self._builder_args.build_dir, ensure_absolute=True
            )

        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)
            if self.allow_print:
                print("Made Dir: " + dist_dir)

        if self._builder_args.pyz_out:
            pyz_mod_name = f"mod_{uuid.uuid4().hex}"
            self._prelude_file = str(self._write_prelude_file(dist_dir, pyz_mod_name))
            dest_file = dist_dir / f"{pyz_mod_name}.pyz"
        else:
            dest_file = dist_dir / f"{self._model.args.output_name}.py"

        self._dest_file = str(dest_file)

        if os.path.exists(self._dest_file):
            os.remove(self._dest_file)
            if self.allow_print:
                print("Deleted File: " + self._dest_file)

        if self._model.args.single_script:
            with open(self._src_file, "r", encoding="utf-8") as s_file:
                output = s_file.read()
            with open(self._dest_file, "w", encoding="utf-8") as output_file:
                output_file.write(output)
        else:
            # get exclude modules, don't worry about duplicates, scriptmerge handles it.
            exclude_modules = (
                self._model.args.exclude_modules + self._config.build_exclude_modules
            )
            output = scriptmerge.script(
                path=str(self._src_file),
                add_python_modules=[],
                add_python_paths=self._get_include_paths(),
                exclude_python_modules=exclude_modules,
                clean=self._model.args.clean,
                pyz_out=self._builder_args.pyz_out,
            )
            if self._builder_args.pyz_out:
                with open(self._dest_file, "wb") as output_file:
                    output_file.write(output)
            else:
                with open(self._dest_file, "w", encoding="utf-8") as output_file:
                    output_file.write(output)
        # endregion Make file using scriptmerge
        # region Append Global Exports

        # endregion Append Global Exports
        # region Report
        if self.allow_print and os.path.exists(self._dest_file):
            print("Generated File: " + self._dest_file)
        if self.allow_print and os.path.exists(self._prelude_file):
            print("Generated File: " + self._prelude_file)
        # endregion Report
        if self._model.args.single_script:
            self._append_g_exported(self._dest_file)
        if self._prelude_file:
            self._append_g_exported(self._prelude_file)
        if self._embed:
            self._embed_scripts(build_dir=dist_dir)
        return True

    # endregion Public Methods

    @property
    def allow_print(self) -> bool:
        return self._allow_print

    @allow_print.setter
    def allow_print(self, value: bool) -> None:
        self._allow_print = value
