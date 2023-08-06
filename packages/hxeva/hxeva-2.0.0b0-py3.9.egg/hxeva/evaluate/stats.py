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

__all__ = ['Stats']

from abc import ABC
from typing import Union, Optional

import numpy as np
from numpy import ndarray, Inf, NaN

from .base import BaseEval


class Stats(BaseEval, ABC):

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
              reduction: str = 'mean',
              vmin: Union[int, float] = -Inf,
              vmax: Union[int, float] = Inf,
              precision: int = 4,
              ) -> dict:
        """ Calculate statistics error.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            method: evaluate method. Default: ``['rmse', 'mae', 'bias']``.
            flag: mask flag, determining whether grid points need to be evaluated. Default: ``None``.
            amin: minimum value of input. Default: ``Negative Inf``.
            amax: maximum value of input Default: ``Inf``.
            left: left interval is closed or not. Default: ``True``.
            right: right interval is closed or not. Default: ``False``.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `none` will return per element.
            vmin: minimum value of result. Default: ``Negative Inf``.
            vmax: maximum value of result. Default: ``Inf``.
            precision: precision of the result. Default: ``4``.

        Returns:
            dict:
                - dictionary of statistic evaluation.
        """

        if method is None:
            method = ('rmse', 'mae', 'bias')
        elif isinstance(method, str):
            method = (method,)
        elif isinstance(method, (list, tuple)):
            method = tuple(method)
        else:
            raise TypeError(f'Expected string or list method for evaluating, but got {type(method)}!')

        # keep data within interval & drop NaN
        flag = cls.drop_miss(input, target, flag=flag, amin=amin, amax=amax, left=left, right=right)

        res = dict()
        for m in method:
            tmp = getattr(cls, m.lower())(input, target, flag, reduction.lower())
            res[m] = (np.clip(np.round(tmp, precision), a_min=vmin, a_max=vmax))
        return res

    @classmethod
    def _reduce(cls,
                data: ndarray,
                reduction: str = 'mean',
                ) -> Union[float, ndarray]:
        if reduction == 'mean':
            if np.sum(~np.isnan(data)) > 0:
                return float(np.nanmean(data))
            else:
                return NaN
        elif reduction == 'none':
            return data
        else:
            raise ValueError(f'Expected got reduction like `mean` or `none`, but got {reduction}!')

    @classmethod
    def cc(cls,
           input: ndarray,
           target: ndarray,
           flag: ndarray,
           reduction: str
           ) -> float:
        """ Correlation Coefficient, `CC or R2 <https://en.wikipedia.org/wiki/Coefficient_of_determination>`_

        Notes:
            :math:`CC = \\frac{\\sum{(y_i - \\overline{truth}) * (f_i - \\overline{test})}}{\\sqrt{\\sum{(y_i - \\overline{truth})^2} * \\sum{(f_i - \\overline{test})^2}}}`

            Range of CC: [-1, 1]. Best score is 1.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            float:
                 - `float` return averaged CC
        """
        if reduction in ['None']:
            raise KeyError('Correlation coefficient cannot supported `None` reduction!')

        if np.sum(flag):
            input, target = input[flag], target[flag]
            input_mean, target_mean = np.mean(input), np.mean(target)

            up = np.sum((target - target_mean) * (input - input_mean))
            down = np.sum((target - target_mean) ** 2 * (input - input_mean) ** 2) ** 0.5
            if down == 0:
                return NaN
            else:
                return up / down
        else:
            return NaN

    @classmethod
    def mae(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Mean Absolute Error, `MAE <https://en.wikipedia.org/wiki/Mean_absolute_error>`_

        Notes:
            :math:`MAE = \\frac{1}{N} * \\sum{\\left|{ f_i - y_i}\\right|}`

            Range of MAE: [0, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged MAE
                - `ndarray` return per MAE
        """
        mae = np.zeros_like(input)
        mae[flag] = np.abs(input - target)[flag]
        mae[~flag] = NaN
        if np.sum(flag):
            return cls._reduce(mae, reduction)
        else:
            return NaN

    @classmethod
    def mbe(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Mean Bias Error, MBE

        Notes:
            :math:`MBE = \\frac{1}{N} * \\sum{(f_i - y_i)}`

            Range of MBE: (-Inf, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged MBE
                - `ndarray` return per MBE
        """
        mbe = np.zeros_like(input)
        mbe[flag] = (input - target)[flag]
        mbe[~flag] = NaN

        if np.sum(flag):
            return cls._reduce(mbe, reduction)
        else:
            return NaN

    @classmethod
    def mbr(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Mean Bias Ratio, MBR

        Notes:
            :math:`MBR = \\frac{1}{N} * \\sum{\\frac{f_i}{y_i}}`

            Range of MBR: (-Inf, Inf). Best score is 1.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged MBR
                - `ndarray` return per MBR
        """
        flag &= target != 0

        mbr = np.zeros_like(input)
        mbr[flag] = input[flag] / target[flag]
        mbr[~flag] = NaN

        if np.sum(flag):
            return cls._reduce(mbr, reduction)
        else:
            return NaN

    @classmethod
    def mape(cls,
             input: ndarray,
             target: ndarray,
             flag: ndarray,
             reduction: str
             ) -> Union[float, ndarray]:
        """ Mean Absolute Percentage Error, `MAPE <https://en.wikipedia.org/wiki/Mean_absolute_percentage_error>`_

        Notes:
            :math:`MAPE = \\frac{1}{N} * \\sum{\\frac{\\left|{f_i - y_i}\\right|}{y_i}}`

            Range of MAPE: [0, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged MAPE
                - `ndarray` return per MAPE
        """
        flag &= target != 0  #
        mre = np.zeros_like(input)
        mre[flag] = np.abs(input - target)[flag] / target[flag]
        mre[~flag] = NaN

        if np.sum(flag):
            return cls._reduce(mre, reduction)
        else:
            return NaN

    @classmethod
    def mpe(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Mean Percentage Error, `MPE <https://en.wikipedia.org/wiki/Mean_percentage_error>`_

        Notes:
            :math:`MPE = \\frac{1}{N} * \\sum{\\frac{(f_i - y_i)}{y_i}}`

            Range of MPE: (-Inf, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged MPE
                - `ndarray` return per MPE
        """
        flag &= target != 0
        mpe = np.zeros_like(input)
        mpe[flag] = (input - target)[flag] / target[flag]
        mpe[~flag] = NaN

        if np.sum(flag):
            return cls._reduce(mpe, reduction)
        else:
            return NaN

    @classmethod
    def mse(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Mean Squared Error, `MSE <https://en.wikipedia.org/wiki/Mean_squared_error>`_

        Notes:
            :math:`MSE = \\frac{1}{N} * \\sum{(f_i - y_i)^2}`

            Range of MSE: [0, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged MSE
                - `ndarray` return per MSE
        """
        mse = np.zeros_like(input)
        mse[flag] = (input - target)[flag] ** 2
        mse[~flag] = NaN

        if np.sum(flag):
            return cls._reduce(mse, reduction)
        else:
            return NaN

    @classmethod
    def nse(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Nash-Sutcliffe Efficiency, `NSE <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020WR027101>`_

        Notes:
            :math:`NSE = 1 - \\frac{MSE}{S_o^2}`
            :math:`MSE = \\frac{1}{N} * \\sum{(f_i - y_i)^2}`
            :math:`S_o^2 = \\frac{1}{N - 1} * \\sum{(y_i - \\overline{truth})^2}`

            Range of NSE: (-Inf, 1]. Best score is 1.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            float:
                - `float` return averaged NSE
        """
        if reduction in ['None']:
            raise KeyError('Correlation coefficient cannot supported `None` reduction!')

        mse = cls.mse(input, target, flag, 'mean')
        so2 = (target[flag] - np.nanmean(target[flag])) / (np.sum(flag) - 1)

        if so2 == 0:
            return NaN
        else:
            return float(1 - mse / so2)

    @classmethod
    def qre(cls,
            input: ndarray,
            target: ndarray,
            flag: ndarray,
            reduction: str
            ) -> Union[float, ndarray]:
        """ Quantified Relative Error, QRE

        Notes:
            :math:`QRE = \\frac{1}{N} * \\sum{\\frac{f_i - y_i}{f_i + y_i}}`

            Range of QRE: (-Inf, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged QRE
                - `ndarray` return per QRE
        """
        flag &= (input + target) != 0

        qre = np.zeros_like(input)
        qre[flag] = (input - target)[flag] / (input + target)[flag]
        qre[~flag] = NaN
        if reduction == 'mean':
            if np.sum(~np.isnan(qre)) > 0:
                return np.power(np.nanmean(qre), 0.5)
            else:
                return NaN
        elif reduction == 'none':
            return cls._reduce(qre, reduction='none')
        else:
            raise ValueError(f'Expected got reduction like `mean` or `none`, but got {reduction}!')

    @classmethod
    def rmse(cls,
             input: ndarray,
             target: ndarray,
             flag: ndarray,
             reduction: str
             ) -> Union[float, ndarray]:
        """ Root Mean Squared Error, `RMSE <https://en.wikipedia.org/wiki/Root-mean-square_deviation>`_

        Notes:
            :math:`RMSE = \\sqrt{\\frac{1}{N} * \\sum{(f_i - y_i) ^ 2}}`

            Range of RMSE: [0, Inf). Best score is 0.0.

        Args:
            input: input data as evaluated product.
            target: target data as ground-truth.
            flag: mask flag, determining whether grid points need to be evaluated.
            reduction: reduction method for result. Default: ``mean``.
                - `mean` will return averaged result.
                - `None` will return per element.

        Returns:
            (float, ndarray):
                - `float` return averaged RMSE
                - `ndarray` return per RMSE
        """
        mse = np.zeros_like(input)
        mse[flag] = (input - target)[flag] ** 2
        mse[~flag] = NaN
        if reduction == 'mean':
            if np.sum(~np.isnan(mse)) > 0:
                return np.power(np.nanmean(mse), 0.5)
            else:
                return NaN
        elif reduction == 'none':
            return cls._reduce(mse, reduction='none')
        else:
            raise ValueError(f'Expected got reduction like `mean` or `none`, but got {reduction}!')
