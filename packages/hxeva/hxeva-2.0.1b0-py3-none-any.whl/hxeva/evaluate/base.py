# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/28   17:19
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['BaseEval']

from abc import ABCMeta, abstractmethod
from typing import Union

import numpy as np
from numpy import ndarray, Inf

def lt(x: Union[int, float, ndarray],
       y: Union[int, float, ndarray]
       ) -> Union[bool, ndarray]:
    return x < y


def le(x: Union[int, float, ndarray],
       y: Union[int, float, ndarray]
       ) -> Union[bool, ndarray]:
    return x <= y


class BaseEval(metaclass=ABCMeta):
    """ Base model for evaluating.

    """

    @classmethod
    @abstractmethod
    def calc(cls,
             input: ndarray,
             target: ndarray,
             **kwargs
             ) -> dict:
        raise NotImplementedError

    @classmethod
    def drop_miss(cls,
                  *args: Union[int, float, ndarray],
                  flag: Union[bool, ndarray, None] = None,
                  amin: Union[int, float] = -np.inf,
                  amax: Union[int, float] = np.inf,
                  left: bool = True,
                  right: bool = False,
                  ) -> ndarray:
        """

        Args:
            *args: input data to be evaluated.
            flag: mask flag, determining whether grid points need to be evaluated. Default: ``None``.
            amin: minimum value of input. Default: ``Negative Inf``.
            amax: maximum value of input Default: ``Inf``.
            left: left interval is closed or not. Default: ``True``.
            right: right interval is closed or not. Default: ``False``.

        Returns:

        """
        left_func = le if left else lt
        right_func = le if right else lt

        # initialize exist flag.
        if flag is None:
            flag = np.ones_like(args[0]).astype(bool)

        # judge value
        for _ in args:
            flag &= left_func(amin, _) & right_func(_, amax)
            flag &= ~np.isnan(_)

        return flag
