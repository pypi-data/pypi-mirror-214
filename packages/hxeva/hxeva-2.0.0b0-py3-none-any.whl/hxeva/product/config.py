# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/25   15:47
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['Config']

from dataclasses import dataclass
import logging
from typing import Optional, Any


def _type_check(key: str,
                file: dict,
                key_type: Any,
                ) -> None:
    tmp = file[key]
    assert isinstance(tmp, key_type), TypeError(f'`{key}` of configuration must be `{key_type}`, '
                                                f'but got {type(tmp)}!')


def _file_config(file: dict) -> dict:
    file_keys = file.keys()
    required_keys = ['name', 'file', 'keys']
    # check required keys
    assert set(required_keys).issubset(set(file_keys)), ValueError('File configuration must contain keys: `name`,'
                                                                   '`file` and `keys`!')
    # check key value
    _type_check('file', file, str)
    _type_check('keys', file, list)

    # Set default value & type check.
    if 'timezone' in file_keys:
        _type_check('timezone', file, str)
        assert file['timezone'] in ['UTC', 'CST'], ValueError(f'Expected `UTC` or `CST`, but got {file["timezone"]}!')
    else:
        file.setdefault('timezone', 'UTC')
    if 'name_Lat' in file_keys:
        _type_check('name_Lat', file, str)
    else:
        file.setdefault('name_Lat', 'Lat')
    if 'name_Lon' in file_keys:
        _type_check('name_Lon', file, str)
    else:
        file.setdefault('name_Lon', 'Lon')

    if 'shape' in file.keys():
        tmp = file['shape']
        assert isinstance(tmp, tuple), TypeError(f'`keys` of configuration must be tuple, but got {type(tmp)}!')
    return file


@dataclass
class Config(object):
    """ configuration of evaluation product, including target file configuration, input file configuration,
    code, keys, location, method and so on.

    Args:
        target_file: configuration of target file.
        input_file: configuration of input file.
        code: product code.
        keys: final unified key name
        loc: area location of data.
        admin_code: administrative code of target area. Default: ``None``.
        area: name of area. Default: ``全市平均``.
        time_list: list of lead time. Default: ``[None]``.
            - `[None]`: observation product.
            - `[timedelta]`: forecast product.
        border: administration border information. Default: ``None``.
        fill_value: value to fill NaN result. Default: ``999``.
        precision: precision of result. Default: ``4``.
        log_level: level of logger.
    """

    def __init__(self,
                 target_file: dict,
                 input_file: dict,
                 code: str,
                 keys: list,
                 loc: dict,
                 admin_code: Optional[int] = None,
                 area: str = '全市平均',
                 time_list: Optional[list] = None,
                 border: Optional[dict] = None,
                 fill_value: int = 999,
                 precision: int = 4,
                 log_level: int = logging.DEBUG,
                 ):
        super(Config, self).__init__()
        # configuration of `target_file` and `input_file`.
        self.target_file: dict = _file_config(target_file)
        self.input_file: dict = _file_config(input_file)

        # configuration of `code`
        assert isinstance(code, str), TypeError(f'`code` of configuration must be `string`, but got {type(code)}!')
        self.code: str = code

        # configuration of `keys`
        assert isinstance(keys, list), TypeError(f'`keys` of configuration must be `list`, but got {type(keys)}!')
        self.keys: list = keys

        # pre-produce configuration of `loc`
        assert isinstance(loc, dict), TypeError(f'`loc` of configuration must be `dict`, but got {type(loc)}!')
        new_loc = dict()
        new_loc['lat1'], new_loc['lat2'] = loc['slat'] - loc['error'], loc['elat'] + loc['error']
        new_loc['lon1'], new_loc['lon2'] = loc['slon'] - loc['error'], loc['elon'] + loc['error']
        self.loc: dict = new_loc

        # configuration of `admin_code`
        self.admin_code: Optional[int] = admin_code

        # configuration of `area`
        self.area: str = area

        # configuration of `time_list`
        if time_list is None:
            time_list = [None]
        self.time_list: list = time_list

        # configuration of `border`
        self.border: Optional[dict] = border

        # configuration of `fill_value`
        self.fill_value: int = fill_value

        # configuration of `precision`
        self.precision: int = precision

        # configuration of `log_level`
        self.log_level: int = log_level
