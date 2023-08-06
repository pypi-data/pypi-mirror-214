# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/28   17:56
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['Space']

from abc import ABC
from functools import reduce
from typing import Union, Optional

import numpy as np
from numpy import ndarray, Inf, NaN
import skimage.measure as ski
from skimage.measure._regionprops import RegionProperties

from .base import BaseEval
from ..meteorology import Distance


class Property:
    """ Property of 2-dimension data.

    Args:
        data: 2-dimension data value. Default: ``None``.
        label: Label connected regions of an integer array from `skimage.measure.label`. Default: ``None``.
        all_prop: Measure properties of labeled image regions from `skimage.measure.regionprops`. Default: ``None``.
        props: Properites from `skimage.measure.regionprops`. Default: ``None``.

    """

    def __init__(self,
                 data: Optional[ndarray] = None,
                 label: Optional[ndarray] = None,
                 all_prop: Optional[RegionProperties] = None,
                 props: Optional[list] = None
                 ):
        self._data = data
        self._label = label
        self._all_prop = all_prop
        self._props = props

    @property
    def data(self):
        return self._data

    @property
    def label(self):
        return self._label

    @property
    def all_prop(self):
        return self._all_prop

    @property
    def props(self):
        return self._props


class Space(BaseEval, ABC):
    """

    """

    @classmethod
    def calc(cls,
             input: ndarray,
             target: ndarray,
             **kwargs
             ) -> dict:
        return cls._calc(input=input, target=target, **kwargs)

    @classmethod
    def _calc(cls,
              input: ndarray,
              target: ndarray,
              method: Union[list, str, None] = None,
              flag: Optional[ndarray] = None,
              amin: Union[int, float] = -Inf,
              amax: Union[int, float] = Inf,
              left: bool = True,
              right: bool = False,
              vmin: Union[int, float] = -Inf,
              vmax: Union[int, float] = Inf,
              precision: int = 4,
              threshold: Union[dict, list] = None,
              min_point: int = 15,
              window_size: tuple = (3, 3),
              ) -> dict:
        """ Calculate space scores.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated. Default: ``None``.
            amin: minimum value of input. Default: ``Negative Inf``.
            amax: maximum value of input Default: ``Inf``.
            left: left interval is closed or not. Default: ``True``.
            right: right interval is closed or not. Default: ``False``.
            vmin: minimum value of result. Default: ``Negative Inf``.
            vmax: maximum value of result. Default: ``Inf``.
            precision: precision of the result. Default: ``4``.
            threshold: the threshold for label. Default: ``[0.1, 999]``.
            min_point: minimum points of the region. Default: ``15``.
            window_size: window size of convolution, unit is point. Default: ``(3, 3)``.

        Returns:
            dict
                - return dictionary with evaluated space.
        """
        if method is None:
            method = ['sal', 'fss']
        elif isinstance(method, str):
            method = method.lower()
            if method in ['fss', 'sal']:
                method = [method]
            else:
                raise KeyError(f'Expected `FSS` or `SAL` method, but got {method}!')
        elif isinstance(method, list):
            _method = list(set(method).intersection({'fss', 'sal'}))
            _difference = list(set(method).difference(_method))
            if len(_difference):
                Warning(f'Space only supports `FSS` and `SAL` method, but got {_difference}')
            method = _method
        else:
            raise TypeError(f'Expected string or list method for evaluating, but got {type(method)}!')

        if threshold is None:
            threshold = dict(sal=[0.1, 999], fss=[0.1])
        elif isinstance(threshold, dict):
            for m in method:
                if m not in threshold:
                    raise KeyError(f'Expected threshold of `{m.upper()}` method, but missed!')
        elif isinstance(threshold, list):
            if len(method) == 1:
                threshold = {method[0]: threshold}
            else:
                raise ValueError(f'Expected threshold of `FSS` and `SAL` methods, but only got one threshold value!')
        elif isinstance(threshold, (float, int)):
            threshold = dict(fss=[threshold])
        else:
            raise ValueError(f'Expected dictionary threshold, but got {type(threshold)}!')

        # keep data within interval & drop NaN
        flag = cls.drop_miss(input, target, flag=flag, amin=amin, amax=amax, left=left, right=right)

        res = dict()
        for m in method:
            if m == 'sal':
                tmp = cls.sal(input, target, flag=flag, threshold=threshold['sal'], min_point=min_point)
                for key, val in tmp.items():
                    tmp[key] = np.clip(round(val, precision), a_min=vmin, a_max=vmax)
                res.update(**tmp)
            elif m == 'fss':
                tmp = cls.fss(input, target, flag=flag, threshold=threshold['fss'], window_size=window_size)
                res[m] = np.clip(np.round(tmp, precision), a_min=vmin, a_max=vmax)
            else:
                raise NotImplementedError
        return res

    @classmethod
    def _calc_props(cls,
                    data: ndarray,
                    flag: ndarray,
                    threshold: Optional[list] = None,
                    min_point: int = 15
                    ) -> Property:
        """ Label connected regions of an integer array within minimum points.

        Args:
            data: input data to be labeled.
            flag: mask flag, determining whether grid points need to be evaluated.
            threshold: the threshold for label.
            min_point: minimum points of the region.

        Returns:
            Property
                - `Property` return property of 2-dimension data.
        """
        if threshold is None:
            threshold = [0.1, 999]

        # Label connected regions of an integer array.
        convert = (np.where((threshold[0] <= data) & (data < threshold[1]), 1, 0) * flag)
        convert = ski.label(convert, connectivity=2, background=0)
        try:
            tmp = ski.regionprops(convert, data)
        except IndexError:
            return Property(data=data, label=convert, all_prop=None, props=[])

        # Remove points less than min_point
        if tmp:
            props = []
            for prop in tmp:
                if prop['area'] >= min_point:
                    props.append(prop)
                else:
                    flag = np.where(convert == prop['label'], 0, 1)
                    convert *= flag
            tmp_prop = ski.regionprops(convert, data)
            if len(tmp_prop):
                return Property(data=data, label=convert, all_prop=tmp_prop[0], props=props)
            else:
                return Property(data=data, label=convert, all_prop=None, props=[])
        else:
            return Property(data=data, label=convert, all_prop=None, props=[])

    @classmethod
    def sal(cls,
            input: ndarray,
            target: ndarray,
            flag: Optional[ndarray] = None,
            threshold: Optional[list] = None,
            min_point: int = 15,
            ) -> dict:
        """ SAL evaluation

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated. Default: ``None``.
            threshold: the threshold for label. Default: ``[0.1, 999]``.
            min_point: minimum points of the region. Default: ``15``.

        Returns:
            dict:
                - dictionary of evaluation SAL.
        """
        assert isinstance(target, ndarray), TypeError(f'Expected `ndarray`, but got the type of target: {type(target)}')
        assert isinstance(input, ndarray), TypeError(f'Expected `ndarray`, but got the type of input: {type(input)}')

        if flag is None:
            flag = np.ones_like(input).astype(bool)

        input = cls._calc_props(input, flag=flag, threshold=threshold, min_point=min_point)
        target = cls._calc_props(target, flag=flag, threshold=threshold, min_point=min_point)

        # SAL evaluation
        res = dict(
            S=cls._s(input, target),
            A=cls._a(input, target),
            L=cls._l(input, target)
        )
        return res

    @classmethod
    def _s(cls,
           input: Property,
           target: Property,
           ) -> float:
        """ structure component S

        Notes:
            :math:`S = \\frac{V(R_f) - V(R_y)}{0.5 * [V(R_f) + V(R_y)]}`

            :math:`V(R) = \\frac{\\sum{R_n * V_n}}{\\sum{R_n}}`

            :math:`V_n = \\frac{\\sum{R_{ij}}}{R_{n}^{max}} = \\frac{R_n}{R_{n}^{max}}`

            where `Rij` are the gridpoint values. `Rn^max` denotes the maximum precipitation value within the object.
            The scaled volume Vn is calculated separately for all objects in the observational and forecast datasets.

        References:
            `SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts. <https://journals.ametsoc.org/view/journals/mwre/136/11/2008mwr2415.1.xml>`_

        Args:
            input: property of input data as evaluated product.
            target: property of target data as ground-truth.

        Returns:
            float:
                - return amplitude component S.
        """

        def scaled_volume(tmp: Property) -> float:
            """Calculate Scaled Volume

            Args:
                tmp
            """
            v = 0
            for prop in tmp.props:
                rn = prop["mean_intensity"] * prop["area"]
                v += rn ** 2 / prop["max_intensity"]
            return v / (tmp.all_prop["mean_intensity"] * tmp.all_prop["area"])

        if (input.all_prop is None) or (target.all_prop is None):
            return NaN
        else:
            input_v = scaled_volume(input)
            target_v = scaled_volume(target)
            return (input_v - target_v) / (target_v + input_v) / 0.5

    @classmethod
    def _a(cls,
           input: Property,
           target: Property,
           ) -> float:
        """ amplitude component A

        Notes:
            :math:`A = \\frac{D(R_f) - D(R_y)}{0.5 * [D(R_f) + D(R_y)]}`

            :math:`D(R) = \\frac{1}{N} * \\sum{R_{ij}}`

            where `Rij` are the gridpoint values.

            Range of L: [-2, 2]. Best score is 0.0.

        References:
            `SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts. <https://journals.ametsoc.org/view/journals/mwre/136/11/2008mwr2415.1.xml>`_

        Args:
            input: property of input data as evaluated product.
            target: property of target data as ground-truth.

        Returns:
            float:
                - return amplitude component A.
        """
        if (input.all_prop is None) or (target.all_prop is None):
            return NaN
        else:
            d_target = target.all_prop["mean_intensity"]
            d_input = input.all_prop["mean_intensity"]
            return (d_input - d_target) / ((d_input + d_target) * 0.5)

    @classmethod
    def _l(cls,
           input: Property,
           target: Property,
           ) -> float:
        """ location component L

        Notes:
            :math:`L = L_1 + L_2`

            :math:`L_1 = \\frac{\\left|{x(R_f) - x(R_y)}\\right|}{d}`

            :math:`L_2 = 2 * \\frac{\\left|{r(R_f) - r(R_y)}\\right|}{d}`

            :math:`r(R) = \\frac{\\sum{R_n * \\left|{x - x_n}\\right|}}{\\sum{R_n}}`

            where d is the largest distance between two boundary points of the considered domain D.
             `x(R)` denotes the center of mass of the precipitation field R within D.


            Range of L: [0, 2]. Best score is 0.0.

        References:
            `SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts. <https://journals.ametsoc.org/view/journals/mwre/136/11/2008mwr2415.1.xml>`_

        Args:
            input: property of input data as evaluated product.
            target: property of target data as ground-truth.
    
        Returns:
            float:
                - return amplitude component L.
        """
        if (input.all_prop is None) or (target.all_prop is None):
            return NaN

        # L1
        # 计算区域内非缺测点的最大距离，这里距离都是用网格点位置而不是经纬度
        convect_union = target.label + input.label
        convect_union[convect_union < 0] = 1
        tmp_prop = ski.regionprops(convect_union, target.data)
        part_l1 = Distance.euclidean(*target.all_prop["centroid"], *input.all_prop["centroid"])

        # L2
        def weighted_distance(tmp: Property) -> float:
            """ Calculate Weighted Averaged Distance.
            Calculate the weighted averaged distance between the centers of mass of the individual objects,
            and the center of mass of the total precipitation field

            Args:
                tmp

            Returns:
                Weighted Averaged Distance
            """
            row, col = tmp.all_prop["centroid"]
            distance = reduce(
                lambda x, y: x + Distance.euclidean(row, col, *y["centroid"]) * y["mean_intensity"] * y["area"],
                [0] + tmp.props)
            return distance / (tmp.all_prop["mean_intensity"] * tmp.all_prop["area"])

        part_l2 = abs(weighted_distance(target) - weighted_distance(input))
        return (part_l1 + part_l2) / Distance.euclidean(*tmp_prop[0]["bbox"])

    @classmethod
    def _window_fss(cls,
                    data: ndarray,
                    i: int,
                    j: int,
                    w_hh: int,
                    w_hw: int,
                    flag: ndarray
                    ) -> float:
        tmp = data[i - w_hh: i + w_hh + 1, j - w_hw: j + w_hw + 1]
        tmp_flag = flag[i - w_hh: i + w_hh + 1, j - w_hw: j + w_hw + 1]
        if np.sum(tmp_flag):
            return float(np.mean(tmp[tmp_flag]))
        else:
            return NaN

    @classmethod
    def fss(cls,
            input: ndarray,
            target: ndarray,
            flag: Optional[ndarray] = None,
            window_size: tuple = (3, 3),
            threshold: Optional[list] = None,
            ) -> ndarray:
        """ Fraction Skill Score, FSS.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated. Default: ``None``.
            window_size: window size of convolution, unit is point. Default: ``(3, 3)``.
            threshold: threshold of evaluated event. Default: ``[0.1]``.

        Returns:
            ndarray:
                - `ndarray` shape like threshold.
        """
        assert isinstance(target, ndarray), TypeError(f'Expected `ndarray`, but got the type of target: {type(target)}')
        assert isinstance(input, ndarray), TypeError(f'Expected `ndarray`, but got the type of input: {type(input)}')

        assert target.ndim == 2, ValueError(f"Expected 2-Dim, but got the dimension of the truth: {target.ndim}")
        assert input.ndim == 2, ValueError(f"Expected 2-Dim, but got the dimension of the test: {input.ndim}")

        assert target.shape == input.shape, ValueError(
            f"Expected the same shape, but the shape of truth - {target.shape}"
            f" is different with test - {input.shape} ")
        if threshold is None:
            threshold = [0.1]

        h, w = input.shape
        w_hh, w_hw = int((window_size[0] - 1) / 2), int((window_size[1] - 1) / 2)
        fss = np.ones_like(threshold) * np.nan
        for index, val in enumerate(threshold):
            truth_hap = np.zeros_like(target)
            truth_hap[target >= val] = 1

            test_hap = np.zeros_like(input)
            test_hap[input >= val] = 1

            a1, a2 = 0, 0
            for i in range(w_hh, h - w_hh):
                for j in range(w_hw, w - w_hw):
                    truth_p = cls._window_fss(truth_hap, i, j, w_hh, w_hw, flag)
                    test_p = cls._window_fss(test_hap, i, j, w_hh, w_hw, flag)
                    if (not np.isnan(truth_p)) and (not np.isnan(test_p)):
                        a1 += (truth_p - test_p) ** 2
                        a2 += truth_p ** 2 + test_p ** 2
            fss[index] = 1 - a1 / (a2 + 1e-10)
        # drop NaN
        fss[fss != fss] = NaN
        return fss
