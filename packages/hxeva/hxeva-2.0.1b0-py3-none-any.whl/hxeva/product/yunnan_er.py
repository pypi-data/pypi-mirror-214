# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/6/8   9:42
----------------------------------
Author     : April
Contact    : fanglwh@foxmail.com
"""

__all__ = ['YUNNANER',
           'YUNNANPRESta', 'YUNNANFactorSta',
           'YUNNANPREGridART', 'YUNNANSpaceGridART',
           ]

from abc import ABC
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
from numpy import NaN
import pygrib

from .art1km import PREGridART, SpaceGridART
from .base import BaseEval
from .config import Config
from .station import PRESta, FactorSta
from ..utils import PathCather


class YUNNANER(BaseEval, ABC):
    def __init__(self,
                 data_cfg: Config,
                 name: str = 'YUNNAN_ER',
                 log_dir: str = './logs',
                 max_counter: int = 1,
                 ):
        super(YUNNANER, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)

    def read_er(self,
                tag_time: datetime,
                lead_time: timedelta,
                skip_bad: bool = False,
                ) -> dict:
        # Read input data as test
        # YunNan - ER file time: report time
        path = Path(PathCather.catch(time=self.transform_time(tag_time - lead_time,
                                                              timezone=self.data_cfg.input_file['timezone']),
                                     lead_time=None, file=self.data_cfg.input_file['file']))
        name = self.data_cfg.input_file['name']
        self.logger.debug(f'[{name}] | path: {path}')

        res = dict(status=True)
        if path.exists():
            with pygrib.open(str(path)) as f:
                message = f.select(parameterName='Total precipitation',
                                   forecastTime=int(lead_time.total_seconds() // 3600) - 1)
                if len(message) == 1:
                    data, lat, lon = message[0].data(**self.data_cfg.loc)
                    res.update({'Lat': lat,
                                'Lon': lon,
                                self.data_cfg.keys[0]: data,
                                })
                    self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
                    return res
        if skip_bad:
            # skip bad data, like missing.
            res['Lon'], res['Lat'] = np.meshgrid(np.linspace(self.data_cfg.loc['lon1'],
                                                             self.data_cfg.loc['lon2'],
                                                             self.data_cfg.input_file['shape'][1]),
                                                 np.linspace(self.data_cfg.loc['lat1'],
                                                             self.data_cfg.loc['lat2'],
                                                             self.data_cfg.input_file['shape'][0]))
            for key in self.data_cfg.keys:
                res[key] = np.full(self.data_cfg.input_file['shape'], NaN)

            # Data is miss
            if lead_time is None:
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
            else:
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time} - {tag_time + lead_time}!')
        else:
            res['status'] = False
            # Data is miss
            if lead_time is None:
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
            else:
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time} - {tag_time + lead_time}!')
        return res


class YUNNANPRESta(PRESta, YUNNANER):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 level: Optional[dict] = None,
                 score_method: str = 'binary',
                 ) -> None:
        super(YUNNANPRESta, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                           method_names=method_names, save=save, threshold=threshold, level=level,
                                           score_method=score_method)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return self.read_er(tag_time, lead_time, skip_bad)


class YUNNANFactorSta(FactorSta, YUNNANER):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 ) -> None:
        super(YUNNANFactorSta, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter,
                                              data_cfg=data_cfg,
                                              method_names=method_names, save=save, threshold=threshold)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return self.read_er(tag_time, lead_time, skip_bad)


class YUNNANPREGridART(PREGridART, YUNNANER):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 level: Optional[dict] = None,
                 score_method: str = 'binary',
                 ):
        super(YUNNANPREGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                               method_names=method_names, save=save, threshold=threshold, level=level,
                                               score_method=score_method)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return self.read_er(tag_time, lead_time, skip_bad)


class YUNNANSpaceGridART(SpaceGridART, YUNNANER):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 min_point: int = 15,
                 ) -> None:
        super(SpaceGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                           method_names=method_names, save=save, threshold=threshold,
                                           min_point=min_point)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return self.read_er(tag_time, lead_time, skip_bad)


class YUNNANERMIN(BaseEval, ABC):
    def __init__(self,
                 data_cfg: Config,
                 name: str = 'YUNNAN_ER_10MIN',
                 log_dir: str = './logs',
                 max_counter: int = 1,
                 ):
        super(YUNNANERMIN, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)

    def read_er(self,
                tag_time: datetime,
                lead_time: timedelta,
                skip_bad: bool = False,
                ) -> dict:
        # Read input data as test
        # YunNan - ER file time: report time
        path = Path(PathCather.catch(time=self.transform_time(tag_time - lead_time,
                                                              timezone=self.data_cfg.input_file['timezone']),
                                     lead_time=None, file=self.data_cfg.input_file['file']))
        name = self.data_cfg.input_file['name']
        self.logger.debug(f'[{name}] | path: {path}')

        res = dict(status=True)
        if path.exists():
            with pygrib.open(str(path)) as f:
                message = f.select(parameterName='Total precipitation',
                                   forecastTime=int(lead_time.total_seconds() // 3600) - 1)
                if len(message) == 1:
                    data, lat, lon = message[0].data(**self.data_cfg.loc)
                    res.update({'Lat': lat,
                                'Lon': lon,
                                self.data_cfg.keys[0]: data,
                                })
                    self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
                    return res
        if skip_bad:
            # skip bad data, like missing.
            res['Lon'], res['Lat'] = np.meshgrid(np.linspace(self.data_cfg.loc['lon1'],
                                                             self.data_cfg.loc['lon2'],
                                                             self.data_cfg.input_file['shape'][1]),
                                                 np.linspace(self.data_cfg.loc['lat1'],
                                                             self.data_cfg.loc['lat2'],
                                                             self.data_cfg.input_file['shape'][0]))
            for key in self.data_cfg.keys:
                res[key] = np.full(self.data_cfg.input_file['shape'], NaN)

            # Data is miss
            if lead_time is None:
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
            else:
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time} - {tag_time + lead_time}!')
        else:
            res['status'] = False
            # Data is miss
            if lead_time is None:
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
            else:
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time} - {tag_time + lead_time}!')
        return res
