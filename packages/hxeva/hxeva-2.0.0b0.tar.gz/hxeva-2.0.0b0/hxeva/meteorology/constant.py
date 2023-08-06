# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/26   15:46
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['Threshold',
           'GRIB2DICT',
           'KELVIN',
           'ER', 'ERA', 'ERB',
           ]

KELVIN = 273.15  # Kelvin zero temperature, Unit: K
ER = 6371.0088  # Radius of Earth, Unit: km
ERA = 6378.137  # Radius of Earth, Unit: km
ERB = 6356.752314245  # Radius of Earth, Unit: km


class Threshold(object):
    """Threshold in meteorology as usual.

    Attributes:
        cref:  Radar reflectivity. Default: ``[-5, 0, 15, 35, 100]``.
        pvalue: Probability value. Default: ``[0, 50, 101]``.
        rain_1h: 1h precipitation. Default: ``[0, 0.1, 2.5, 8.0, 16.0, 150]``.
        rain_3h: 3h precipitation. Default: ``[0, 0.1, 3, 10, 20, 50, 70, 300]``.
        rain_6h: 6h precipitation. Default: ``[0, 0.1, 4, 13, 25, 60, 120, 999]``.
        rain_12h: 12h precipitation. Default: ``[0, 0.1, 5, 15, 30, 70, 140, 999]``.
        rain_24h: 24h precipitation. Default: ``[0, 0.1, 10, 25, 50, 100, 250, 999]``.
        snow_1h: 1h precipitation as snow. Default: ``[0, 0.1, 0.2, 0.5, 0.7, 100]``.
        snow_3h: 3h precipitation as snow. Default: ``[0, 0.1, 0.3, 0.6, 1.5, 100]``.
        snow_6h: 6h precipitation as snow. Default: ``[0, 0.1, 0.5, 1.5, 3.0, 100]``.
        snow_12h: 12h precipitation as snow. Default: ``[0, 0.1, 1.0, 3.0, 6.0, 100]``.
        snow_24h: 24h precipitation as snow. Default: ``[0, 0.1, 2.5, 5.0, 10.0, 100]``.
        rain_level:

    """
    cref = [-5, 0, 15, 35, 100]
    pvalue = [0, 50, 101]
    rain_1h = [0, 0.1, 2.5, 8.0, 16.0, 150]
    rain_3h = [0, 0.1, 3, 10, 20, 50, 70, 300]
    rain_6h = [0, 0.1, 4, 13, 25, 60, 120, 999]
    rain_12h = [0, 0.1, 5, 15, 30, 70, 140, 999]
    rain_24h = [0, 0.1, 10, 25, 50, 100, 250, 999]
    snow_1h = [0, 0.1, 0.2, 0.5, 0.7, 100]
    snow_3h = [0, 0.1, 0.3, 0.6, 1.5, 100]
    snow_6h = [0, 0.1, 0.5, 1.5, 3.0, 100]
    snow_12h = [0, 0.1, 1.0, 3.0, 6.0, 100]
    snow_24h = [0, 0.1, 2.5, 5.0, 10.0, 100]

    rain_level = {"1": "small", "2": "mid", "3": "big", "4": "storm"}


class GRIB2DICT(object):
    """Dictionary of meteorological variables for loading from GRIB2 file.
    """
    PRE_1h = dict(parameterName='Total precipitation')
    rain = dict(parameterName='Total precipitation', level=0, stepType='instant')
    tp = dict(parameterName='Total precipitation', level=0, stepType='accum')
    tem = dict(parameterName='Temperature', level=2, stepType='instant')
    sp = dict(parameterName='Pressure', level=0, stepType='instant')
    rhu = dict(parameterName='Relative humidity', level=2, stepType='instant')
    u = dict(parameterName='u-component of wind', level=10, stepType='instant')
    v = dict(parameterName='v-component of wind', level=10, stepType='instant')
