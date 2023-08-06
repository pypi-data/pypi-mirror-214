# coding: utf-8


__all__ = ["sub_matrices", "pool2d"]

from typing import Tuple, Union

import numpy as np
from numpy import ndarray


def sub_matrices(x: ndarray,
                 window_size: tuple,
                 stride: tuple
                 ) -> ndarray:
    """ Get a strided sub-matrices view of an ndarray.
    
    Args:
    
    
    See Also:
        skimage.util.shape.view_as_windows()
    """
    m, n = x.shape
    sm_x, sn_x = x.strides
    km, kn = window_size
    sm, sn = stride
    # view_shape = (1 + (m - km) // sm, 1 + (n - kn) // sn, km, kn) + x.shape[2:]
    view_shape = (1 + (m - km) // sm, 1 + (n - kn) // sn, km, kn)
    # strides = (sm * sm_x, sn * sn_x, sm_x, sn_x) + x.strides[2:]
    strides = (sm * sm_x, sn * sn_x, sm_x, sn_x)
    return np.lib.stride_tricks.as_strided(x, view_shape, strides=strides)


def pool2d(data: ndarray,
           window_size: Union[int, Tuple[int, int]],
           stride: Union[None, Tuple[int, int]] = None,
           method: str = 'max',
           pad: bool = False
           ) -> ndarray:
    """ Overlapping pooling on 2D or 3D data.
    
    
    Args:
        data: data to be pooled， shape being like (m, n).
        window_size: the window size of pooling, shape being like (km, kn).
        stride: stride of pooling, shape being like (sm, sn). Default: ``(km, kn)``.
        method: method of pooling. Default: ``max``.   默认为 ``max`` 。 池化的方法，可选择为 ``max`` 或 ``mean`` 两种池化方法。
            - ``max``: maximum value of window.
            - ``mean``: average value of window.
        pad: padding result with the same shape of input data. Default: ``False``.
            - ``True``: pad the result, whose shape is like (m // sm, n // sn)
            - ``False``: do not pad the result, whose shape is like  ((m - km) // sm + 1, (n - kn) // sn + 1).

    Returns:
        ndarry:
            - return pooled data with pooling method.
    """
    assert data.ndim == 2, ValueError(f'Expected 2-D input data, but got {data.ndim}-D input data!')
    m, n = data.shape
    if isinstance(window_size, tuple):
        km, kn = window_size
    elif isinstance(window_size, int):
        km, kn = window_size, window_size
    else:
        raise TypeError(f'Expected ``tuple`` or ``int`` of window_size, but got {type(window_size)}!')
    
    if stride is None:
        stride = (km, kn)
    sm, sn = stride

    if pad:
        size = (m - sm + km, n - sn + kn) + data.shape[2:]
        data_pad = np.full(size, np.nan)
        data_pad[km // 2:m + km // 2, kn // 2:n + kn // 2, ...] = data
    else:
        data_pad = data[:(m - km) // sm * sm + km, :(n - kn) // sn * sn + kn, ...]
    
    view = sub_matrices(data_pad, (km, kn), (sm, sn))
    
    if method == 'max':
        return np.nanmax(view, axis=(2, 3))
    elif method == 'mean':
        return np.nanmean(view, axis=(2, 3))
    else:
        raise ValueError(f'Expected ``mean`` or ``max`` method, but got {method}!')
