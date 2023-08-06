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

__all__ = ['Score',
           'ContingencyTable']

from abc import ABC
from collections import namedtuple
from typing import Optional, Union, Callable

import numpy as np
from numpy import ndarray, Inf, NaN

from .base import BaseEval

ContingencyTable = namedtuple("ContingencyTable", ["tp", "fp", "fn", "tn"], defaults=(None, None, None, None))
"""
"""
ContingencyTable.tp.__doc__ = "int: Number of hitting. There is no matching classification while it is -1. Default ``None`` "
ContingencyTable.fp.__doc__ = "int: Number of missing. There is no matching classification while it is -1. Default ``None`` "
ContingencyTable.fn.__doc__ = "int: Number of far alarm. There is no matching classification while it is -1. Default ``None`` "
ContingencyTable.tn.__doc__ = "int: Number of negative correct. There is no matching classification while it is -1. Default ``None`` "


class _WindDirection(object):
    @classmethod
    def classify(cls,
                 input: ndarray,
                 target: ndarray,
                 flag: ndarray,
                 num: int = 8,
                 ) -> ndarray:
        """ Classify wind direction into score table.

        Args:
            input: input wind direction as evaluated product.
            target: target wind direction as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            num: numbers of wind direction to be classified. Default: ``8``.

        Returns:
            ndarray:
                - return wind direction score table.
        """

        assert input.shape == target.shape, ValueError('Expected got the same shape data, '
                                                       f'but got input: {input.shape} and target: {target.shape}!')

        assert input.shape == flag.shape, ValueError(f'Expected got the same shape of mask flag, but got {flag.shape}')

        input = cls.transform(input, num)
        target = cls.transform(target, num)

        table = np.zeros_like(input)
        table[abs(input - target) > 2] = 0.0  # Wind Speed Score 0.0
        table[abs(input - target) == num - 1] = 0.6  # Wind Speed Score 0.6
        table[abs(input - target) == 1] = 0.6  # Wind Speed Score 0.6
        table[input == target] = 1.0  # Wind Speed Score 1.0

        # Mark missing or error data as NaN
        table[~flag | (np.isnan(input)) | (np.isnan(target))] = NaN
        return table

    @classmethod
    def transform(cls,
                  data: ndarray,
                  num: int = 8,
                  ) -> ndarray:
        """ Transform wind direction into wind level. Default left interval is closed and right is open.

        Args:
            data: input wind direction to be transformed.
            num: numbers of wind direction to be classified. Default: ``8``.

        Returns:
            ndarray:
                - return wind direction transform level.
        """
        offset = 360 / num / 2
        res = data % 360 // offset  # keep direction in 0 ~ 360 deg & transform into levels.
        res[res == num * 2 - 1] = -1  # the last level should be near the first level
        res += 1  # positive all levels
        res = res // 2  # two level merged into one on final.
        return res


class _WindSpeed(object):
    @classmethod
    def classify(cls,
                 input: ndarray,
                 target: ndarray,
                 flag: ndarray,
                 threshold: Optional[list] = None,
                 ) -> ndarray:
        """ Classify wind speed into score table.

        Args:
            input: input wind speed as evaluated product.
            target: target wind speed as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            threshold: wind speed threshold list. Default: ``Beaufort Wind Force Scale``.

        Returns:
            ndarray:
                - return wind speed score table.
        """

        assert input.shape == target.shape, ValueError('Expected got the same shape data, '
                                                       f'but got input: {input.shape} and target: {target.shape}!')

        assert input.shape == flag.shape, ValueError(f'Expected got the same shape of mask flag, but got {flag.shape}')

        input = cls.transform(input, threshold)
        target = cls.transform(target, threshold)

        table = np.zeros_like(input)
        table[abs(input - target) > 2] = 0.0  # Wind Speed Score 0.0
        table[abs(input - target) == 2] = 0.4  # Wind Speed Score 0.4
        table[abs(input - target) == 1] = 0.6  # Wind Speed Score 0.6
        table[input == target] = 1.0  # Wind Speed Score 1.0

        # Mark missing or error data as NaN
        table[(~flag) | (np.isnan(input)) | (np.isnan(target))] = NaN
        return table

    @classmethod
    def transform(cls,
                  data: ndarray,
                  threshold: Optional[list] = None,
                  ) -> ndarray:
        """ Transform wind speed into wind level.

        Args:
            data: input wind speed to be transformed.
            threshold: wind speed threshold list. Default: ``Beaufort Wind Force Scale``.

        Returns:
            ndarray:
                - return wind speed transform level.
        """
        if threshold is None:
            # Default: Beaufort Wind Force Scale
            threshold = [0, 0.3, 1.6, 3.4, 5.5, 8.0, 10.8, 13.9, 17.2, 20.8, 24.5, 28.5, 32.7, 37.0, 41.5, 999]

        res = np.zeros_like(data)
        for lvl, thr in enumerate(threshold):
            res[data >= thr] = lvl
        # Mark unexpected value as NaN.
        res[(data < threshold[0]) | (data > threshold[-1])] = NaN
        return res

    @classmethod
    def bias(cls,
             input: ndarray,
             target: ndarray,
             flag: ndarray,
             ) -> ndarray:
        """ Judge wind speed bias.

        Args:
            input: input wind speed as evaluated product.
            target: target wind speed as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.

        Returns:
            ndarray:
                - return wind speed bias.
        """
        assert input.shape == target.shape, ValueError('Expected got the same shape data, '
                                                       f'but got input: {input.shape} and target: {target.shape}!')

        assert input.shape == flag.shape, ValueError(f'Expected got the same shape of mask flag, but got {flag.shape}')
        bias = np.zeros_like(input)
        bias[input < target] = -1
        bias[input > target] = 1
        bias[(~flag) | (input < 0) | (999 < input) | (target < 0) | (999 < target)] = NaN
        return bias


class Score(BaseEval, ABC):
    """ Calculate scores for evaluating product or neural network.

    """
    _WSMETHODS = ('acs', 'scs', 'fss', 'fws')
    _WDMETHODS = ('acd', 'scd')
    _NORMALMETHODS = ('acc', 'bias', 'ets', 'far', 'hss', 'nb', 'po', 'pod', 'precision', 'ra', 'rd', 'sr', 'ts')

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
              threshold: Union[float, int, tuple],
              method: Union[list, str, None] = None,
              flag: Optional[ndarray] = None,
              amin: Union[int, float] = -Inf,
              amax: Union[int, float] = Inf,
              left: bool = True,
              right: bool = False,
              precision: int = 4,
              ) -> dict:
        """ calculate scores.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            threshold: threshold list required for classification into contingency table.
            method: evaluate method. Default: ``['ts', 'po', 'far']``.
            flag: mask flag, determining whether grid points need to be evaluated. Default: ``None``.
            amin: minimum value of input. Default: ``Negative Inf``.
            amax: maximum value of input Default: ``Inf``.
            left: left interval is closed or not. Default: ``True``.
            right: right interval is closed or not. Default: ``False``.
            precision: precision of the result. Default: ``4``.

        Returns:
            dict:
                - return dictionary with evaluated scores.
        """
        if method is None:
            method = ('ts', 'po', 'far')
        elif isinstance(method, str):
            method = (method,)
        elif isinstance(method, (list, tuple)):
            method = tuple(method)
        else:
            raise TypeError(f'Expected string or list method for evaluating, but got {type(method)}!')

        # keep data within interval & drop NaN
        flag = cls.drop_miss(input, target, flag=flag, amin=amin, amax=amax, left=left, right=right)

        res = dict()

        if len(set(method).intersection(set(cls._WSMETHODS))) > 0:
            # calculate transform wind speed
            _method = tuple(set(method).intersection(set(cls._WSMETHODS)))
            _difference = tuple(set(method).difference(set(_method)))
            if len(_difference) > 0:
                Warning(f'Expected evaluating wind speed, but got unexpected method {_difference}')
            table = _WindSpeed.classify(input, target, flag=flag)
            # calculate wind speed forecast weaker or server.
            _bias_method = tuple(set(_method).intersection({'fws', 'fss'}))
            if len(_bias_method) > 0:
                bias = _WindSpeed.bias(input, target, flag=flag)
                for m in _bias_method:
                    res[m] = round(getattr(cls, m.lower())(bias), precision)
            _method = tuple(set(_method).difference(set(_bias_method)))
        elif len(set(method).intersection(set(cls._WDMETHODS))) > 0:
            # calculate transform wind speed
            _method = tuple(set(method).intersection(set(cls._WDMETHODS)))
            _difference = tuple(set(method).difference(set(_method)))
            if len(_difference) > 0:
                Warning(f'Expected evaluating wind direction, but got unexpected method {_difference}')
            table = _WindDirection.classify(input, target, flag=flag)
        else:
            # calculate classify contingency table
            _method = tuple(set(method).intersection(set(cls._NORMALMETHODS)))
            _difference = tuple(set(method).difference(set(_method)))
            if len(_difference) > 0:
                Warning(f'Expected evaluating scores, but got unexpected method {_difference}')
            table = cls.classify(input, target, flag, threshold)

        for m in _method:
            res[m] = round(getattr(cls, m.lower())(table), precision)
        return res

    @classmethod
    def classify(cls,
                 input: ndarray,
                 target: ndarray,
                 flag: ndarray,
                 threshold: Union[float, int, tuple],
                 ) -> ContingencyTable:
        """

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            threshold: threshold list required for classification into contingency table.

        Returns:
            ContingencyTable
                - return classification contingency table.
        """
        assert input.shape == target.shape, ValueError('Expected got the same shape data, '
                                                       f'but got input: {input.shape} and target: {target.shape}!')

        assert input.shape == flag.shape, ValueError(f'Expected got the same shape of mask flag, but got {flag.shape}')

        if isinstance(threshold, (float, int)):
            threshold = (threshold, 999)
        elif isinstance(threshold, tuple):
            pass
        else:
            raise TypeError(f'Expected got tuple threshold to classify, but got {type(threshold)}!')

        if np.sum(flag) > 0:
            input, target = input[flag], target[flag]
            input_pos = (threshold[0] <= input) & (input < threshold[1])  # positive input
            target_pos = (threshold[0] <= target) & (target < threshold[1])  # positive target
            input_neg = ~input_pos  # negative input
            target_neg = ~target_pos  # negative target
            return ContingencyTable(tp=int(np.sum(target_pos & input_pos)),
                                    fp=int(np.sum(target_neg & input_pos)),
                                    fn=int(np.sum(target_pos & input_neg)),
                                    tn=int(np.sum(target_neg & input_neg)),
                                    )
        else:
            return ContingencyTable(tp=-1, fp=-1, fn=-1, tn=-1)

    @classmethod
    def _accuracy(cls,
                  table: ndarray
                  ) -> float:
        """Calculate accuracy of wind.

        Notes:
            :math:`accuracy = \\frac{1}{N} * \\sum{accuracy_i}`

        Args:
            table: wind score table.

        Returns:
            float:
                - Accuracy of wind
        """
        return float(np.nanmean(table.astype(int)))

    @classmethod
    def _wind_score(cls,
                    table: ndarray
                    ) -> float:
        """Calculate score of wind.

        Notes:
            :math:`score = \\frac{1}{N} * \\sum{score_i}`

        Args:
            table: wind score table.

        Returns:
            float:
                - score of wind
        """
        return float(np.nanmean(table))

    @classmethod
    def acd(cls,
            table: ndarray
            ) -> float:
        """ Accuracy of wind direction, ACd.

        Notes:
            :math:`ACd = \\frac{1}{N} * \\sum{ACd_i}`

        Args:
            table: wind direction score table.

        Returns:
            float:
                - ACd
        """
        _flag = np.isnan(table)
        if np.sum(_flag):
            return cls._accuracy(table)
        else:
            return NaN

    @classmethod
    def scd(cls,
            table: ndarray
            ) -> float:
        """ Score of wind direction, SCd.

        Notes:
            :math:`SCd = \\frac{1}{N} * \\sum{SCd_i}`

        Args:
            table: wind direction score table.

        Returns:
            float:
                - SCd
        """
        _flag = np.isnan(table)
        if np.sum(_flag):
            return cls._wind_score(table)
        else:
            return NaN

    @classmethod
    def acs(cls,
            table: ndarray
            ) -> float:
        """ Accuracy of wind speed, ACs.

        Notes:
            :math:`ACs = \\frac{1}{N} * \\sum{ACs_i}`

        Args:
            table: wind speed score table.

        Returns:
            float:
                - ACs
        """
        _flag = np.isnan(table)
        if np.sum(_flag):
            return cls._accuracy(table)
        else:
            return NaN

    @classmethod
    def scs(cls,
            table: ndarray
            ) -> float:
        """ Score of wind speed, SCs.

        Notes:
            :math:`SCs = \\frac{1}{N} * \\sum{SCs_i}`

        Args:
            table: wind speed score table.

        Returns:
            float:
                - SCs
        """
        _flag = np.isnan(table)
        if np.sum(_flag):
            return cls._wind_score(table)
        else:
            return NaN

    @classmethod
    def fss(cls,
            bias: ndarray
            ) -> float:
        """ Rate of forecast Server wind speed, FSs.

        Notes:
            :math:`FSs = \\frac{1}{N} * \\sum{server_i}`

        Args:
            bias: wind speed bias.

        Returns:
            float:
                - FSs
        """
        _flag = np.isnan(bias)
        if np.sum(_flag):
            bias[bias == -1] = 0  # mask forecast weaker
            return float(np.nanmean(bias))
        else:
            return NaN

    @classmethod
    def fws(cls,
            bias: ndarray
            ) -> float:
        """ Rate of forecast weaker wind speed, FWs.

        Notes:
            :math:`FWs = \\frac{1}{N} * \\sum{weaker_i}`

        Args:
            bias: wind speed bias.

        Returns:
            float:
                - FWs
        """
        _flag = np.isnan(bias)
        if np.sum(_flag):
            bias[bias == 1] = 0  # mask forecast server
            return float(np.nanmean(bias))
        else:
            return NaN

    @classmethod
    def _score(cls,
               table: ContingencyTable,
               func: Callable[[ContingencyTable], float],
               ) -> float:
        if table.count(None) > 0:
            Warning(f"Expected ContingencyTable for calculating scores, but table have not been calculated yet!")
            return NaN
        elif table.count(-1) == 4:
            Warning(f"There is no matching classification, please choose other levels!")
            return NaN
        else:
            return func(table)

    @classmethod
    def acc(cls,
            table: ContingencyTable
            ) -> float:
        """Accuracy

        Notes:
            :math:`accuracy = \\frac{tp + tn}{tp + fp + fn + tn}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - Accuracy
        """

        def calc_acc(_table: ContingencyTable) -> float:
            if sum(_table) > 0:
                return (_table.tp + _table.tn) / sum(_table)
            else:
                return NaN

        return cls._score(table=table, func=calc_acc)

    @classmethod
    def bias(cls,
             table: ContingencyTable
             ) -> float:
        """Bias score

        Notes:
            :math:`Bias = \\left|\\frac{tp + fp}{tp + fn} - 1\\right|`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - Bias score
        """

        def calc_bias(_table: ContingencyTable) -> float:
            if _table.tp + _table.fn > 0:
                return abs((_table.tp + _table.fp) / (_table.tp + _table.fn) - 1)
            else:
                return NaN

        return cls._score(table=table, func=calc_bias)

    @classmethod
    def ets(cls,
            table: ContingencyTable
            ) -> float:
        """ Equitable Threat Score, ETS

        Notes:
            :math:`ETS = \\frac{tp -ra}{tp + fp + fn + tn - ra}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - ETS
        """
        ra = cls.ra(table)
        if np.isnan(ra):
            return NaN
        if table.tp + table.fp + table.fn - ra:
            return table.tp / (table.tp + table.fp + table.fn - ra)
        else:
            return NaN

    @classmethod
    def far(cls,
            table: ContingencyTable
            ) -> float:
        """ False Alarm Rate, FAR.

        Notes:
            :math:`FAR = \\frac{fp}{tp + fp}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - FAR
        """

        def calc_far(_table: ContingencyTable) -> float:
            if (_table.fp + _table.tp) > 0:
                return _table.fp / (_table.fp + _table.tp)
            else:
                return NaN

        return cls._score(table=table, func=calc_far)

    @classmethod
    def hss(cls,
            table: ContingencyTable
            ) -> float:
        """ Heidke Skill Score, HSS.

        Notes:
            :math:`expect = \\frac{(tp + fn) * (tp + fp) + (tn + fn) * (tn + fp)}{tp + fp + fn + tn}`

            :math:`HSS = \\frac{tp + tn - expect}{tp + fp + fn + tn - expect}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - HSS
        """
        ra = cls.ra(table)
        rd = cls.rd(table)
        if np.isnan(ra) or np.isnan(rd):
            return NaN
        if sum(table) - ra - rd:
            return (table.tp + table.tn - ra - rd) / (sum(table) - ra - rd)
        else:
            return NaN

    @classmethod
    def nb(cls,
           table: ContingencyTable
           ) -> float:
        """ Normalized bias.

        Notes:
            :math:`expect = \\frac{(tp + fn) * (tp + fp) + (tn + fn) * (tn + fp)}{tp + fp + fn + tn}`

            :math:`HSS = \\frac{tp + tn - expect}{tp + fp + fn + tn - expect}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - NB
        """

        def calc_nb(_table: ContingencyTable) -> float:
            if (_table.tp + _table.fp) * (_table.tp + _table.fn) == 0:
                return NaN
            else:
                return np.exp(-1 * np.abs(np.log((_table.tp + _table.fp) / (_table.tp + _table.fn))))

        return cls._score(table=table, func=calc_nb)

    @classmethod
    def po(cls,
           table: ContingencyTable
           ) -> float:
        """ Underreporting Rate, PO.

        Notes:
            :math:`PO = \\frac{fn}{tp + fn}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - PO
        """

        def calc_po(_table: ContingencyTable) -> float:
            if (_table.tp + _table.fn) > 0:
                return _table.fn / (_table.tp + _table.fn)
            else:
                return NaN

        return cls._score(table=table, func=calc_po)

    @classmethod
    def pod(cls,
            table: ContingencyTable
            ) -> float:
        """ Probability of Detection, POD.

        Notes:
            :math:`POd = \\frac{tp}{tp + fn}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - POD
        """

        def calc_pod(_table: ContingencyTable) -> float:
            if (_table.tp + _table.fn) > 0:
                return _table.tp / (_table.tp + _table.fn)
            else:
                return NaN

        return cls._score(table=table, func=calc_pod)

    @classmethod
    def ra(cls,
           table: ContingencyTable
           ) -> float:
        """ra.

        Notes:
            :math:`ra = \\frac{(tp + fp) * (tp + fn)}{tp + fp + fn + tn}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - ra
        """

        def calc_ra(_table: ContingencyTable) -> float:
            if sum(_table) > 0:
                return (_table.tp + _table.fp) * (_table.tp + _table.fn) / sum(_table)
            else:
                return NaN

        return cls._score(table=table, func=calc_ra)

    @classmethod
    def rd(cls,
           table: ContingencyTable
           ) -> float:
        """rd.

        Notes:
            :math:`rd = \\frac{(tn + fp) * (tn + fn)}{tp + fp + fn + tn}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - rd
        """

        def calc_rd(_table: ContingencyTable) -> float:
            if sum(_table) > 0:
                return (_table.tn + _table.fp) * (_table.tn + _table.fn) / sum(_table)
            else:
                return NaN

        return cls._score(table=table, func=calc_rd)

    @classmethod
    def sr(cls,
           table: ContingencyTable
           ) -> float:
        """Success Rate, SR.

        Notes:
            :math:`SR = \\frac{tp}{tp + fp}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - SR
        """

        def calc_sr(_table: ContingencyTable) -> float:
            if (_table.tp + _table.fp) > 0:
                return _table.tp / (_table.tp + _table.fp)
            else:
                return NaN

        return cls._score(table=table, func=calc_sr)

    @classmethod
    def ts(cls,
           table: ContingencyTable
           ) -> float:
        """ Threat Score, TS.

        Notes:
            :math:`TS = \\frac{tp}{tp + fp + fn}`

        Args:
            table: contingency table, including values: :obj:`tp`, :obj:`fp`, :obj:`fn` and :obj:`tn`.

        Returns:
            float:
                - TS
        """

        def calc_sr(_table: ContingencyTable) -> float:
            if (_table.tp + _table.fp + _table.fn) > 0:
                return _table.tp / (_table.tp + _table.fp + _table.fn)
            else:
                return NaN

        return cls._score(table=table, func=calc_sr)
