# coding: utf-8
from enum import Enum


class ModelTypeEnum(str, Enum):
    EXAMPLE = "EXAMPLE"
    AUTO = "AUTO"

    def __str__(self):
        return self.value
