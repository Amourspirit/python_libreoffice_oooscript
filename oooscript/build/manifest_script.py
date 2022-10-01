# coding: utf-8
"""
Manages write script elments into manifest xml
"""
import xml.dom.minidom
from xml.dom.minicompat import NodeList
from pathlib import Path
from typing import Iterable
from ..cfg import config
from typing import cast
from ..lib.ex import ManifestError


class ManifestScript:
    def __init__(self, manifest_path: Path, script_name: str) -> None:
        """
        Constructor

        Args:
            manifest_path (Path): Path to manifest.xml file
            script_name (str): Name of script that is to be embed in document.
        """
        self._path = manifest_path
        self._script_name = script_name
        self._config = config.get_app_cfg()

    def read(self) -> xml.dom.minidom.Document:
        domtree = xml.dom.minidom.parse(str(self._path))
        return domtree

    def write(self, verify=True) -> None:
        """
        Adds Script elements to manifest.xml file.
        """
        ns = self._config.xml_manifest_namespace

        domtree = self.read()
        group = cast(xml.dom.minidom.Element, domtree.documentElement)
        # ns = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
        nl = cast(NodeList, group.getElementsByTagNameNS(ns, "file-entry"))

        changed = False
        if not self._contains(ns, nl, f"Scripts/python/{self._script_name}", ""):
            el_scripts_full = cast(xml.dom.minidom.Element, domtree.createElementNS(ns, "manifest:file-entry"))
            el_scripts_full.setAttributeNS(ns, "manifest:full-path", f"Scripts/python/{self._script_name}")
            el_scripts_full.setAttributeNS(ns, "manifest:media-type", "")
            group.appendChild(el_scripts_full)
            changed = True

        if not self._contains(ns, nl, f"Scripts/python/"):
            el_scripts_python = cast(xml.dom.minidom.Element, domtree.createElementNS(ns, "manifest:file-entry"))
            el_scripts_python.setAttributeNS(ns, "manifest:full-path", "Scripts/python/")
            el_scripts_python.setAttributeNS(ns, "manifest:media-type", "application/binary")
            group.appendChild(el_scripts_python)

            el_scripts = cast(xml.dom.minidom.Element, domtree.createElementNS(ns, "manifest:file-entry"))
            el_scripts.setAttributeNS(ns, "manifest:full-path", "Scripts/")
            el_scripts.setAttributeNS(ns, "manifest:media-type", "application/binary")
            group.appendChild(el_scripts)
            changed = True

        if verify:
            if not self.verify(domtree):
                raise ManifestError("Validaition failed")

        if changed:
            # only write if there have been additions
            with open(self._path, "w") as file:
                domtree.writexml(writer=file)

    def verify(self, manifest: xml.dom.minidom.Document) -> bool:
        attribs = cast(NodeList, manifest.getElementsByTagName("manifest:file-entry"))
        if attribs is None:
            return False
        if not self._contains_attribs(attribs=attribs, name_fp="manifest:full-path", value_fp=f"Scripts/python/{self._script_name}", name_mp="manifest:media-type", value_mp=""):
            return False
        if not self._contains_attribs(attribs=attribs, name_fp="manifest:full-path", value_fp="Scripts/python/", name_mp="manifest:media-type", value_mp="application/binary"):
            return False
        if not self._contains_attribs(attribs=attribs, name_fp="manifest:full-path", value_fp="Scripts/", name_mp="manifest:media-type", value_mp="application/binary"):
            return False
        
        return True

    def _contains(
        self,
        ns: str,
        lst: Iterable[xml.dom.minidom.Element],
        full_path: str,
        media_type: str = "application/binary",
    ) -> bool:
        result = False
        for el in lst:
            fp: xml.dom.minidom.Attr = el.getAttributeNodeNS(ns, "full-path")
            if not fp:
                continue
            mt: xml.dom.minidom.Attr = el.getAttributeNodeNS(ns, "media-type")
            if mt is None:
                continue
            if fp.value == full_path and mt.value == media_type:
                result = True
                break

        return result
    
    def _contains_attribs(self, attribs: NodeList, name_fp: str, value_fp:str, name_mp: str, value_mp: str) -> bool:
        result = False
        for atr in attribs:
            el = cast(xml.dom.minidom.Element, atr)
            fp = el.getAttribute(name_fp)
            if fp == value_fp:
                mt = el.getAttribute(name_mp)
                if mt == value_mp:
                    result = True
                    break
        return result
