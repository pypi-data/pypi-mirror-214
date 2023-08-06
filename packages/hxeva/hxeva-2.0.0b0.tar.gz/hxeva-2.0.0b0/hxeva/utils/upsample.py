# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/25   15:46
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['UpSample']

import numpy as np
from scipy.ndimage import zoom


class UpSample(object):
    def __init__(self, times=None) -> None:
        if times is None:
            times = [1, 2, 2]
        self.times = times


class KronUpSample(UpSample):
    def transform(self, a):
        return np.kron(a, np.ones(self.times))


class Spline1UpSample(UpSample):
    """bilinear"""
    def transform(self, a):
        return zoom(a, self.times, order=1)


class Spline3UpSample(UpSample):
    """cubic"""
    def transform(self, a):
        return zoom(a, self.times, order=3)

