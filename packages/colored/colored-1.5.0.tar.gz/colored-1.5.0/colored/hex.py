#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .library import hex_colors


def HEX(color) -> str:
    """ Contribution by Fredrik Klasson """

    # Extend shorthand #ABC -> #AABBCC, like in CSS
    if len(color) == 4:
        color = '#'+color[1]*2+color[2]*2+color[3]*2

    # Try an exact lookup, trying to favor lower numbers
    # (e.g. find 10 instead of 46 for #00FF00)
    for code, hex_color in hex_colors.items():
        if hex_color == color:
            return code

    # Try to find nearest match using a simple least squares fit.
    # We could try to factor in human perception bias by weighting
    # as suggested by <https://stackoverflow.com/a/1847112> but for
    # now lets just KISS and make upp our minds later, no?
    # (we do skip the sqrt since we just care for the relative value)

    # The reference color
    r, g, b = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))

    cube = lambda x: x * x

    f = lambda hex_val, ref: cube(int(hex_val, 16) - ref)

    min_cube_d = cube(0xFFFFFF)
    nearest = '15'

    for k, h in hex_colors.items():
        cube_d = f(h[1:3], r) + f(h[3:5], g) + f(h[5:7], b)
        if cube_d < min_cube_d:
            min_cube_d = cube_d
            nearest = k

    return nearest
