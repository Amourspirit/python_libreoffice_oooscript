
# coding: utf-8
import os
# importing using a text file as version source is not supported when packaging scripts using stickytape.
with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r", encoding="utf-8") as f:
    __version__ = f.read().strip()
