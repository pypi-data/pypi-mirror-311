#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import warnings
import platform
from enum import Enum

"""
unknown platform use print() function
"""

__all__ = []


_PLATFORM_NAME = platform.system()


class ColorForeground(Enum):
    BLACK = None
    RED = None
    GREEN = None
    YELLOW = None
    BLUE = None
    PINK = None
    CYAN = None
    WHITE = None

    BRIGHT_BLACK = None
    BRIGHT_RED = None
    BRIGHT_GREEN = None
    BRIGHT_YELLOW = None
    BRIGHT_BLUE = None
    BRIGHT_PINK = None
    BRIGHT_CYAN = None
    BRIGHT_WHITE = None


class ColorBackground(Enum):
    BLACK = None
    RED = None
    GREEN = None
    YELLOW = None
    BLUE = None
    PINK = None
    CYAN = None
    WHITE = None

    BRIGHT_BLACK = None
    BRIGHT_RED = None
    BRIGHT_GREEN = None
    BRIGHT_YELLOW = None
    BRIGHT_BLUE = None
    BRIGHT_PINK = None
    BRIGHT_CYAN = None
    BRIGHT_WHITE = None


class Style(Enum):
    RESET_ALL = None
    BOLD = None
    WEAKENED = None
    ITALIC = None
    UNDERLINE = None
    SLOW_FLUSH = None
    FAST_FLUSH = None
    REDISPLAY = None


def _dye(*objects, sep=' ', end="\n", flush: bool = False, file=sys.stdout,
         fc: ColorForeground = None, bc: ColorBackground = None, style: Style = None):
    warnings.warn(f"color output not support platform: {_PLATFORM_NAME}, use print() function.",
                  category=RuntimeWarning, stacklevel=1, source=None)
    content = sep.join([str(obj) for obj in objects])
    file.write(content + end)
    if flush is True:
        file.flush()
