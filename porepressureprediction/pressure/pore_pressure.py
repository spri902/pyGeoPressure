# -*- coding: utf-8 -*-
"""
Routines to calculate pore pressure
"""
from __future__ import division, print_function, absolute_import

__author__ = "yuhao"

import numpy as np


def bowers(v, obp, u, fe_idx, a, b, vmax):
    """
    Compute pressure using Bowers equation.

    Parameters
    ----------
    v : 1-d ndarray
        velocity array whose unit is m/s.
    obp : 1-d ndarray
        Overburden pressure whose unit is Pa.
    v0 : float, optional
        the velocity of unconsolidated regolith whose unit is m/s.
    a : float, optional
        coefficient a
    b : float, optional
        coefficient b

    Notes
    -----
    .. math:: P = OBP - [\\frac{(V-V_{0})}{a}]^{\\frac{1}{b}}
    """
    sigma_max = ((vmax-1524)/a)**(1/b)
    ves = ((v - 1524) / a)**(1.0 / b)
    ves_fe = sigma_max*(((v-1524)/a)**(1/b)/sigma_max)**u
    ves[fe_idx:] = ves_fe[fe_idx:]
    return obp - ves


def virgin_curve(sigma, a, b):
    "Virgin curve in Bowers' method."
    v0 = 1524
    return v0 + a * sigma**b


def unloading_curve(sigma, a, b, u, v_max):
    "Unloading curve in Bowers's method."
    sigma_max = ((v_max-1524)/a)**(1/b)
    independent = sigma_max*(sigma/sigma_max)**(1/u)
    return virgin_curve(independent, a, b)


def eaton(v, vn, hydrostatic, lithostatic, n=3):
    """
    Compute pore pressure using Eaton equation.

    Parameters
    ----------
    v : 1-d ndarray
        velocity array whose unit is m/s.
    vn : 1-d ndarray
        normal velocity array whose unit is m/s.
    hydrostatic : 1-d ndarray
        hydrostatic pressure in mPa
    lithostatic : 1-d ndarray
        Overburden pressure whose unit is mPa.
    v0 : float, optional
        the velocity of unconsolidated regolith whose unit is ft/s.
    n : float, optional
        eaton exponent

    Notes
    -----
    .. math:: P = OBP - VES_{n}* a (\\frac{V}{V_{n}})^{b}
    """
    ves = (lithostatic - hydrostatic) * (v / vn)**n
    pressure = lithostatic - ves
    return pressure


def fillipino():
    pass


def invert_multivariate_virgin(vel, phi, vsh, a_0, a_1, a_2, a_3, B):
    """
    Calculate effective stress using multivariate virgin curve

    Parameters
    ----------
    vel : 1-d ndarray
        velocity array whose unit is m/s.
    phi : 1-d ndarray
        porosity array
    vsh : 1-d ndarray
        shale volume
    a_0, a_1, a_2, a_3 : scalar
        coefficients

    Returns
    -------
    sigma: 1-d ndarray
    """
    return ((vel - a_0 + a_1 * phi + a_2 * vsh) / a_3)**(1 / B)

def multivariate_virgin(sigma, phi, vsh, a_0, a_1, a_2, a_3, B):
    """
    Calculate velocity using multivariate virgin curve
    """
    return a_0 - a_1 * phi - a_2 * vsh + a_3 * sigma**B
