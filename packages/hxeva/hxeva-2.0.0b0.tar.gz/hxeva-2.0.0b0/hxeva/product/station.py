# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/24   10:42
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""
__all__ = ['StationEval', 'PRESta', 'FactorSta',
           ]

from abc import ABC
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
from numpy import NaN
import pandas as pd

from .base import BaseEval, ScoreEval, StatsEval, select_admin
from .config import Config
from ..utils import PathCather


class StationEval(BaseEval, ABC):
    mode = 'Station'

    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 ):
        super(StationEval, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        # Read target data as truth
        path = Path(PathCather.catch(time=self.transform_time(tag_time, timezone=self.data_cfg.target_file['timezone']),
                                     lead_time=None, file=self.data_cfg.target_file['file']))
        name = self.data_cfg.target_file["name"]
        _columns = ['Station_Id_C', 'Admin_Code_CHN', 'Province', 'City', 'Cnty', 'Lat', 'Lon']

        self.logger.debug(f'[{name}]| path: {path}')
        res = dict(status=True)
        if path.exists():
            data = pd.read_csv(path, sep='\t', low_memory=False, on_bad_lines='skip')
            flag = select_admin(data, self.data_cfg.admin_code)
            data = data.loc[flag, _columns + self.data_cfg.target_file['keys']]
            data.reset_index(drop=True, inplace=True)
            res.update({'dataframe': data,
                        'Lat': np.array(data.Lat),
                        'Lon': np.array(data.Lon)
                        })
            for new_key, old_key in zip(self.data_cfg.keys, self.data_cfg.target_file['keys']):
                res.update({new_key: np.array(data[old_key])})
            self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
        else:
            # Data is miss
            if skip_bad:
                # skip bad data, like missing.
                for key in self.data_cfg.keys:
                    res[key] = np.array([NaN])
                tmp = pd.DataFrame(columns=_columns + self.data_cfg.target_file['keys'])
                tmp.loc[0, :] = -1
                res['dataframe'] = tmp
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
            else:
                res['status'] = False
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
        return res

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        input = self.read_data(tag_time, lead_time=lead_time, file=self.data_cfg.input_file, skip_bad=skip_bad)
        if input['status']:
            for old_key, new_key in zip(self.data_cfg.input_file['keys'], self.data_cfg.keys):
                input[new_key] = input[old_key].copy()
        return input


class PRESta(ScoreEval, StationEval, ABC):
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
        super(PRESta, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                     method_names=method_names, save=save, threshold=threshold, level=level,
                                     score_method=score_method)
        self.mode = StationEval.mode


class FactorSta(StatsEval, StationEval, ABC):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 ) -> None:
        super(FactorSta, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                        method_names=method_names, save=save, threshold=threshold)
        self.mode = StationEval.mode
