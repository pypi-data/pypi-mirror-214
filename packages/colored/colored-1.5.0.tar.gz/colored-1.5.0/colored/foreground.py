#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .library import format_codes, colors
from .exceptions import InvalidColor


class MetaFore(type):
    """ Overrides AttributeError when __getattr__ called. """
    def __getattr__(cls, color):
        raise InvalidColor(f'{InvalidColor.__name__}: {color}')


class Fore(metaclass=MetaFore):

    ESC: str = format_codes['ESC']
    END: str = format_codes['END']
    FORE: str = format_codes['FORE']

    for color, code in colors.items():
        vars()[color] = f'{ESC}{FORE}{code}{END}'

    # Make color name uppercase.
    for color, code in colors.items():
        vars()[color.upper()] = f'{ESC}{FORE}{code}{END}'
