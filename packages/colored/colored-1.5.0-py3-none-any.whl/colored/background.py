#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .library import format_codes, colors
from .exceptions import InvalidColor


class MetaBack(type):
    """ Overrides AttributeError when __getattr__ called. """
    def __getattr__(cls, color):
        raise InvalidColor(f'{InvalidColor.__name__}: {color}')


class Back(metaclass=MetaBack):

    ESC: str = format_codes['ESC']
    END: str = format_codes['END']
    BACK: str = format_codes['BACK']

    for color, code in colors.items():
        vars()[color] = f'{ESC}{BACK}{code}{END}'

    # Make color name uppercase.
    for color, code in colors.items():
        vars()[color.upper()] = f'{ESC}{BACK}{code}{END}'
