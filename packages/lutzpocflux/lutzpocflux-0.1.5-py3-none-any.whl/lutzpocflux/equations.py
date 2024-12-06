import math
import numpy as np

def prd(x: float) -> float:
    """
    Calculates labile fraction of export pr_d given seasonal variation index (SVI)

    Args:
        x (float): Seasonal variation index (SVI)

    Returns:
        float: labile fraction of export pr_d
    """
    return ((31 * x**2) + (49 * x) + 7.8) * (10**-3)


def rld(x: float) -> float:
    """
    Calculates remineralization length scale rl_d given seasonal variation index (SVI)

    Args:
        x (float): Seasonal variation index (SVI)

    Returns:
        float: remineralization length scale rl_d
    """
    return 1400 * math.exp(-0.54 * x)


def prr(x: float) -> float:
    """
    Calculates refractory and rapidly sinking fraction of export pr_r given seasonal
    variation index (SVI)

    Args:
        x (float): Seasonal variation index (SVI)

    Returns:
        float: refractory and rapidly sinking fraction of export pr_r
    """
    return ((2.6 * x**2) - (4.2 * x) + 4.8) * (10**-3)


def pratioze(prd_l: float, ze: float, rld_l: float, prr_l: float) -> float:
    """
    Calculates the labile and refractory components of flux to depth below the export zone depth ze
    (depth z minus export zone depth).

    Args:
        prd_l (float): labile fraction of export pr_d
        ze (float): depth below the export zone depth
        rld_l (float): remineralization length scale rl_d
        prr_l (float): refractory and rapidly sinking fraction of export pr_r

    Returns:
        float: export flux ratio
    """
    return prd_l * math.exp(-ze / rld_l) + prr_l


prd_f = np.vectorize(prd)
rld_f = np.vectorize(rld)
prr_f = np.vectorize(prr)
pratioze_f = np.vectorize(pratioze)
