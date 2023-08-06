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
__all__ = ['GridEval', 'PREGrid', 'FactorGrid', 'SpaceGrid']

from abc import ABC
from datetime import datetime, timedelta
from typing import Optional

from .base import BaseEval, ScoreEval, StatsEval, SpaceEval
from .config import Config


class GridEval(BaseEval, ABC):
    mode = 'Grid'

    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 ):
        super(GridEval, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        target = self.read_data(tag_time, lead_time=None, file=self.data_cfg.target_file, skip_bad=skip_bad)
        name = self.data_cfg.target_file['name']
        if target['status']:
            self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
            for old_key, new_key in zip(self.data_cfg.target_file['keys'], self.data_cfg.keys):
                target[new_key] = target[old_key].copy()
        else:
            self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
        return target

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


class PREGrid(ScoreEval, GridEval, ABC):
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
        super(PREGrid, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                      method_names=method_names, save=save, threshold=threshold, level=level,
                                      score_method=score_method)
        self.mode = GridEval.mode


class FactorGrid(StatsEval, GridEval, ABC):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 ) -> None:
        super(FactorGrid, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                         method_names=method_names, save=save, threshold=threshold)
        self.mode = GridEval.mode


class SpaceGrid(SpaceEval, GridEval, ABC):
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
        super(SpaceGrid, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                         method_names=method_names, save=save, threshold=threshold, min_point=min_point)
        self.mode = GridEval.mode
