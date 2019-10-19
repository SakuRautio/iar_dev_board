#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum, auto, unique

@unique
class ErrorCode(Enum):
	WTF = -1
	OK = 0
	NOT_IMPLEMENTED = auto()
	INCORRECT_PARAMETERS = auto()
	IAR_FAIL = auto()
	OS_FAIL = auto()
	GIT_FAIL = auto()
	PARSE_FAIL = auto()
