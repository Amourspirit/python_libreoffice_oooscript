# coding: utf-8
from pydantic import BaseModel, validator, Field
from typing import List
from .args import CfgArgs
from .. import validators
from ...lib.enums import AppTypeEnum


class ModelScriptCfg(BaseModel):
    id: str
    version: str
    app: AppTypeEnum
    name: str
    args: CfgArgs
    methods: List[str] = Field(default_factory=list)
    _str_null_empty = validator("name", allow_reuse=True)(validators.str_null_empty)

    @validator("id")
    def validate_id(cls, value: str) -> str:
        if value == "oooscript":
            return value
        raise ValueError(f"root/id/ must be 'oooscript'. Current value: {value}")
