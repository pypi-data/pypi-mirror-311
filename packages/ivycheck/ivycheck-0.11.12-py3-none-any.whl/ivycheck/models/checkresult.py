"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
from .entitymatch import EntityMatch
from dataclasses_json import Undefined, dataclass_json
from ivycheck import utils
from typing import List, Optional


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class CheckResult:
    UNSET='__SPEAKEASY_UNSET__'
    passed: Optional[bool] = dataclasses.field(default=UNSET, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('passed'), 'exclude': lambda f: f is CheckResult.UNSET }})
    r"""Indicates if the check passed or failed. If None, the check failed to run."""
    score: Optional[float] = dataclasses.field(default=UNSET, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('score'), 'exclude': lambda f: f is CheckResult.UNSET }})
    r"""A numerical score representing the result of the check, if applicable."""
    message: Optional[str] = dataclasses.field(default=UNSET, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('message'), 'exclude': lambda f: f is CheckResult.UNSET }})
    r"""A descriptive message about the check result."""
    findings: Optional[List[EntityMatch]] = dataclasses.field(default=UNSET, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('findings'), 'exclude': lambda f: f is CheckResult.UNSET }})
    r"""A list of entities or issues found during the check. Each entity is detailed with its type, matched text, and positions."""
    sanitized_output: Optional[str] = dataclasses.field(default=UNSET, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('sanitized_output'), 'exclude': lambda f: f is CheckResult.UNSET }})
    r"""The cleaned or transformed output, where sensitive or problematic data is masked or altered."""
    

