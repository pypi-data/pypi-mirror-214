# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/25   15:27
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['ART1KM', 'PREGridART', 'FactorGridART', 'SpaceGridART']

from abc import ABC
from datetime import datetime, timedelta
from typing import Optional

from .base import BaseEval
from .config import Config
from .grid import PREGrid, FactorGrid, SpaceGrid


class ART1KM(BaseEval, ABC):
    def __init__(self,
                 data_cfg: Config,
                 name: str = 'ART_1KM',
                 log_dir: str = './logs',
                 max_counter: int = 1,
                 ):
        super(ART1KM, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)
        self.mode = 'Grid'

    def read_art1km(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        """Read ART-1KM 10min data as target, which is need to accumulate with six files.

        Args:
            tag_time: target time of target file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of ART-1KM
        """
        name = self.data_cfg.target_file['name']
        target = dict()

        for minutes in range(0, 60, 10):
            tmp = self.read_data(tag_time - timedelta(minutes=minutes),
                                 lead_time=None, file=self.data_cfg.target_file, skip_bad=skip_bad)
            if tmp['status']:
                self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time - timedelta(minutes=minutes)}!')

                if len(target):
                    # accumulate precipitation pre-10min
                    for key in self.data_cfg.target_file['keys']:
                        target[key] += tmp[key]
                else:
                    # initialize target with first ART-1KM
                    target.update(tmp)
            else:
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time - timedelta(minutes=minutes)}!')
                return tmp
        # change key from `file-keys` into  `keys`
        for old_key, new_key in zip(self.data_cfg.target_file['keys'], self.data_cfg.keys):
            target[new_key] = target[old_key]
        return target


class PREGridART(PREGrid, ART1KM):
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
        super(PREGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                         method_names=method_names, save=save, threshold=threshold, level=level,
                                         score_method=score_method)

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        return super(PREGridART, self).read_art1km(tag_time, skip_bad)


class FactorGridART(FactorGrid, ART1KM):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 ):
        super(FactorGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                            method_names=method_names, save=save, threshold=threshold)

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        return super(FactorGridART, self).read_art1km(tag_time, skip_bad)


class SpaceGridART(SpaceGrid, ART1KM):
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

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        return super(SpaceGridART, self).read_art1km(tag_time, skip_bad)
