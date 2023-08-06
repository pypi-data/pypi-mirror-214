#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .library import format_codes, styles
from .exceptions import InvalidStyle


class MetaStyle(type):
    """ Overrides AttributeError when __getattr__ called. """
    def __getattr__(cls, color):
        raise InvalidStyle(f'{InvalidStyle.__name__}: {color}')


class Style(metaclass=MetaStyle):

    ESC: str = format_codes['ESC']
    END: str = format_codes['END']

    for style, code in styles.items():
        vars()[style] = f'{ESC}{code}{END}'

    # Make color name uppercase.
    for style, code in styles.items():
        vars()[style.upper()] = f'{ESC}{code}{END}'
