# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/24   11:24
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['read_border',
           'select_admin']

from pathlib import Path
from typing import Union, Optional

from netCDF4 import Dataset
import numpy as np
from numpy import ndarray
import pandas as pd
from pandas.core.frame import DataFrame


def _nc_border(path: Path,
               vname: str = 'qxCode',
               name_lat: str = 'lat',
               name_lon: str = 'lon',
               loc: Optional[dict] = None,
               ) -> dict:
    """ Read NetCDF-4 administration information.

    Args:
        path: path of NetCDF-4 file.
        vname: name of variable name.
        name_lat: name of latitude.
        name_lon: name of longitude.
        loc: area location of data.

    Returns:

    """
    tmp = Dataset(path)
    b_lat = tmp.variables[name_lat][:]
    b_lon = tmp.variables[name_lon][:]
    if isinstance(loc, dict):
        nx = np.where((loc['slon'] <= b_lon) & (b_lon <= loc['elon']))[0]
        ny = np.where((loc['slat'] <= b_lat) & (b_lat <= loc['elat']))[0]
        b_code = tmp.variables[vname][ny, nx]
        b_lon, b_lat = np.meshgrid(b_lon[nx], b_lat[ny])
    else:
        b_code = tmp.variables[vname][:]
    if vname == 'qxCode':
        pass
    elif vname == 'dsCode':
        b_code = b_code // 100
    else:
        pass
    return dict(Code=b_code, Lat=b_lat, Lon=b_lon)


def _txt_border(path: Path
                ) -> dict:
    """

    Args:
        path:

    Returns:

    """
    if path.suffix == '.csv':
        tmp = pd.read_csv(path, low_memory=False, on_bad_lines='skip')
    elif path.suffix == '.txt':
        tmp = pd.read_csv(path, sep='\t', low_memory=False, on_bad_lines='skip')
    else:
        raise ValueError(f'Expected text format of administration, but got {path.suffix}!')
    return dict(List=tmp)


def read_border(path: Union[str, Path, list],
                vname: str = 'qxCode',
                name_lat: str = 'lat',
                name_lon: str = 'lon',
                loc: Optional[dict] = None,
                ) -> dict:
    """ read border information.

    Args:
        path: path or paths of border information.
        vname: variable name of netCDF4 border information.
        name_lat: latitude name of netCDF4 border information.
        name_lon: longitude name of netCDF4 border information.
        loc: location of border information.

    Returns:
        dict:
            - dictionary of border information
    """

    if isinstance(path, list):
        path = [Path(tmp_path) for tmp_path in path]
    elif isinstance(path, str):
        path = [Path(path)]
    elif isinstance(path, Path):
        path = [path]
    else:
        raise ValueError(f'Expected path list of administration files, but got {path}!')

    border = dict()
    for p in path:
        if p.suffix == '.nc':
            border.update(_nc_border(p, vname=vname, name_lon=name_lon, name_lat=name_lat, loc=loc))
        elif p.suffix in ['.txt', '.csv']:
            border.update(_txt_border(p))
        else:
            raise ValueError(f'Cannot read format of {p.suffix}, which is {str(p)}.')
    return border


def select_admin(data: DataFrame,
                 admin_code: Optional[int]
                 ) -> ndarray:
    """ select administration from station data whose format is text.

    Args:
        data: station data.
        admin_code: administration code of target area.

    Returns:
        ndarray:
            - the flag of target administration masked as `True`.
    """
    if admin_code is None:
        flag = np.ones_like(data.Admin_Code_CHN).astype(bool)
    elif admin_code < 100:
        flag = data.Admin_Code_CHN.astype(int) // 10000 == admin_code
    elif admin_code < 10000:
        flag = data.Admin_Code_CHN.astype(int) // 100 == admin_code
    elif admin_code < 100000:
        flag = data.Admin_Code_CHN.astype(int) == admin_code
    else:
        raise ValueError(f'Admin code is less than 1000000, but got {admin_code}!')
    return flag