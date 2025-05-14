"""
Module for loading and validating configuration.
"""
import json
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel, EmailStr, ValidationError, Field


class TriggerRule(BaseModel):
    keyword: str
    email: EmailStr


class Config(BaseModel):
    sources: list[str]
    profile: Dict[str, float]
    triggers: list[TriggerRule]
    delivery_email: EmailStr
    daily_limit: int = Field(10, ge=1)
    schedule_time: str  # 'HH:MM'


def load_config(path: str = './config.json') -> Config:
    data = json.loads(Path(path).read_text())
    try:
        return Config(**data)
    except ValidationError as ex:
        raise RuntimeError(f"Invalid config: {ex}")