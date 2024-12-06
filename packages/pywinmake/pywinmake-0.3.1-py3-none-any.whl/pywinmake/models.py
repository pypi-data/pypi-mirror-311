#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2024 Savoir-faire Linux

Models for the pywinmake package.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class BuildStatus(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class BuildResult:
    status: BuildStatus
    message: str
    error: Optional[Exception] = None

    @classmethod
    def success(cls, message: str) -> 'BuildResult':
        return cls(BuildStatus.COMPLETED, message)

    @classmethod
    def failure(cls, message: str, error: Optional[Exception] = None) -> 'BuildResult':
        return cls(BuildStatus.FAILED, message, error)