# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/15   10:27
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['BaseEval', 'MidEval',
           'ScoreEval', 'StatsEval', 'SpaceEval'
           ]

from abc import ABCMeta, abstractmethod, ABC
from datetime import datetime, timedelta
import logging
from pathlib import Path
from time import sleep
from typing import Optional

import pandas as pd
from netCDF4 import Dataset
import numpy as np
from numpy import ndarray, Inf, NaN
import pygrib

from .config import Config
from ..evaluate import Score, Stats, Space
from ..log import CustomFormatter
from ..meteorology import Threshold
from ..utils import PathCather, select_admin, unified_shape


class BaseEval(metaclass=ABCMeta):
    """ Basic evaluate class to running evaluation product.
    Inspection products are obtained mainly through the function ``main``.

    Args:
        name: name of evaluation product.
        log_dir: directory of logger. Default: ``./logs``.
        max_counter: maximum number of counter to break evaluation. Default: ``1``.
        data_cfg: configuration of input data and target dat.
    """

    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 ) -> None:
        super(BaseEval, self).__init__()
        self.name: str = name
        self.log_dir: Path = Path(log_dir)
        self.max_counter: int = max_counter
        self.data_cfg: Config = data_cfg

        self.logger: Optional[logging.Logger] = None

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.mode = None

    @property
    def _grib_dict(self) -> dict:
        """dictionary information to read file whose format is GRIB2."""
        return dict(PRE_1h=dict(parameterName="Total precipitation"),
                    rain=dict(parameterName="Total precipitation", level=0, stepType="instant"),
                    tp=dict(parameterName="Total precipitation", level=0, stepType="accum"),
                    tem=dict(parameterName="Temperature", level=2, stepType="instant"),
                    sp=dict(parameterName="Pressure", level=0, stepType="instant"),
                    rhu=dict(parameterName="Relative humidity", level=2, stepType="instant"),
                    u=dict(parameterName="u-component of wind", level=10, stepType="instant"),
                    v=dict(parameterName="v-component of wind", level=10, stepType="instant"),
                    )

    def transform_time(self,
                       time: datetime,
                       timezone: str,
                       rollback: bool = False
                       ) -> datetime:
        """ transform timezone of time into UTC from original timezone.

        Args:
            time: original time.
            timezone: original timezone of time.
            rollback: rollback transform, meaning all calculating is reversed. Default: ``False``.

        Returns:
            datetime:
                - rollback is ``False``, return time of UTC.
                - rollback is ``True``, return time of input timezone.
        """
        flag = -1 if rollback else 1

        assert isinstance(timezone, str), TypeError('Expected string timezone, '
                                                    f'but got {type(timezone)} of {timezone}.')
        # timezone
        if timezone in ['UTC', 'GMT']:
            time_area = 0  # UTC
        elif timezone in ['CST', 'BJS']:
            time_area = 8  # UTC+8
        else:
            raise NotImplementedError(f'{timezone} has not implemented yet')

        return time + timedelta(hours=flag * time_area)

    @abstractmethod
    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        """ read target file as ground-truth.

        Args:
            tag_time: target time of target file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of target data.
        """
        raise NotImplementedError

    @abstractmethod
    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        """ read input file as test, which would be evaluated.

        Args:
            tag_time: target time of input file.
            lead_time: lead time of input file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of input data.
        """
        raise NotImplementedError

    def _read_nc(self,
                 path: str,
                 file: dict,
                 skip_bad: bool = False,
                 ) -> dict:
        """ read data whose file format is ``NetCDF``.

        Args:
            path: file path.
            file: configuration of file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of data.
        """
        name = file['name']
        data = dict(status=True)
        tmp = Dataset(path)
        # original coordination.
        tmp_lat = tmp.variables[file['name_Lat']][:]
        tmp_lon = tmp.variables[file['name_Lon']][:]

        # select area in location.
        num_lat = np.where((self.data_cfg.loc['lat1'] <= tmp_lat) & (tmp_lat <= self.data_cfg.loc['lat2']))[0]
        num_lon = np.where((self.data_cfg.loc['lon1'] <= tmp_lon) & (tmp_lon <= self.data_cfg.loc['lon2']))[0]

        # coordination in location & grid into 2-D
        data['Lon'], data['Lat'], = np.meshgrid(tmp_lon[num_lon], tmp_lat[num_lat])

        # keys data in location.
        for key in file['keys']:
            if key in tmp.variables.keys():
                data[key] = tmp.variables[key][num_lat, num_lon]
            elif skip_bad:
                data[key] = np.full(file['shape'], NaN)
                self.logger.warning(f'[{name}]| Miss {key} in data: {path} - but continue to evaluate')
            else:
                data['status'] = False
                self.logger.warning(f'[{name}]| Miss {key} in data: {path}')
        return data

    def _read_grb(self,
                  path: str,
                  file: dict,
                  skip_bad: bool = False,
                  ) -> dict:
        """ read data whose file format is ``GIRB2``.

        Args:
            path: file path.
            file: configuration of file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of data.
        """
        name = file['name']
        data = dict(status=True)
        # read from GRIB2
        with pygrib.open(path) as f:
            for key in file['keys']:
                tmp = f.select(**self._grib_dict[key])
                if len(tmp) > 0:
                    tmp_data, tmp_lat, tmp_lon = tmp[0].data(**self.data_cfg.loc)
                elif skip_bad:
                    tmp_data = np.full(file['shape'], NaN)
                    tmp_lon, tmp_lat = np.meshgrid(np.linspace(self.data_cfg.loc['lon1'],
                                                               self.data_cfg.loc['lon2'],
                                                               file['shape'][1]),
                                                   np.linspace(self.data_cfg.loc['lat1'],
                                                               self.data_cfg.loc['lat2'],
                                                               file['shape'][0]),
                                                   )
                    self.logger.warning(f'[{name}]| Miss {key} in data: {path}')
                else:
                    data['status'] = False
                    self.logger.warning(f'[{name}]| Miss {key} in data: {path}')
                    continue
                # key data in location.
                data[key] = tmp_data
                # coordination in location.
                data['Lat'], data['Lon'] = tmp_lat, tmp_lon
        return data

    def read_data(self,
                  tag_time: datetime,
                  lead_time: Optional[timedelta],
                  file: dict,
                  skip_bad: bool = False,
                  ) -> dict:
        """ read data, only support file format in ``NetCDF`` or ``GRIB2``.

        Args:
            tag_time: target time of file.
            lead_time: lead time of file.
            file: configuration of file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of data.
        """
        # Read input data as test
        path = Path(PathCather.catch(time=self.transform_time(tag_time, timezone=file['timezone']),
                                     lead_time=lead_time, file=file['file']))
        name = file['name']
        self.logger.debug(f'[{name}] | path: {path}')
        if path.exists():
            if path.suffix.lower() == '.nc':
                return self._read_nc(str(path), file=file, skip_bad=skip_bad)
            elif path.suffix.lower() == '.grb2':
                return self._read_grb(str(path), file=file, skip_bad=skip_bad)
            else:
                raise NotImplementedError(f'Expected file format is `NetCDF` or `GRIB2`, but got {path.suffix}!')
        else:
            data = dict(status=True)
            if skip_bad:
                # skip bad data, like missing.
                data['Lon'], data['Lat'] = np.meshgrid(np.linspace(self.data_cfg.loc['lon1'],
                                                                   self.data_cfg.loc['lon2'],
                                                                   file['shape'][1]),
                                                       np.linspace(self.data_cfg.loc['lat1'],
                                                                   self.data_cfg.loc['lat2'],
                                                                   file['shape'][0]))
                for key in file['keys']:
                    data[key] = np.full(file['shape'], NaN)

                # Data is miss
                if lead_time is None:
                    self.logger.warning(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
                else:
                    self.logger.warning(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time} - {tag_time + lead_time}!')
            else:
                data['status'] = False
                # Data is miss
                if lead_time is None:
                    self.logger.warning(f'[{name}]| MISS DATA in time: {tag_time}!')
                else:
                    self.logger.warning(f'[{name}]| MISS DATA in time: {tag_time} - {tag_time + lead_time}!')
            return data

    def _log(self,
             new_time: str,
             old_time: str
             ) -> None:
        """ produce product logger.

        Args:
            new_time: new log file time to create.
            old_time: old log file time to delete.
        """
        if self.logger is None:
            self.logger = logging.Logger(name=self.name, level=self.data_cfg.log_level)

        # Delete log file that is out of the retention time range.
        old_path = self.log_dir.joinpath(f'{old_time}.log')
        old_path.unlink(missing_ok=True)

        # New log file that is target time.
        if self.logger.handlers:
            self.logger.handlers.pop()
        new_handler = logging.FileHandler(self.log_dir.joinpath(f'{new_time}.log'), mode='w')
        new_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(new_handler)

    def evaluate(self,
                 tag_time: datetime,
                 skip_bad: bool = False,
                 ) -> bool:
        raise NotImplementedError

    def main(self,
             tag_time: datetime,
             delay: timedelta = timedelta(minutes=20),
             log_fmt: str = "%Y%m%d%H",
             log_days: int = 7,
             ) -> None:
        """ main function for product evaluation.

        Args:
            tag_time: target time to evaluate.
            delay: delay time to evaluate for data delay or something others, unit: ``minutes``. Default: ``20 minutes``.
            log_fmt: date time format of log filename. Default: ``%Y%m%d%H``.
            log_days: length of log file retention, unit: ``day``. Default: ``7 days``.
        """

        # log file produce
        old_time: str = (tag_time - timedelta(days=log_days)).strftime(log_fmt)
        new_time: str = tag_time.strftime(log_fmt)
        self._log(new_time=new_time, old_time=old_time)

        st = datetime.now()
        # tag_time + delay to run product
        if (tag_time + delay) > st:
            delta = (tag_time + delay - st).total_seconds()
            self.logger.info(f'Sleep {delta:.1f} s ')
            sleep(delta)

        st = datetime.now()
        # until evaluate is normally done with `True` return.
        counter = 0
        while True:
            if self.evaluate(tag_time=tag_time, skip_bad=False):
                break
            counter += 1
            sleep(15)
            if counter > self.max_counter:
                self.evaluate(tag_time=tag_time, skip_bad=True)
                self.logger.warning(f'Skip bad data in time: {tag_time}.')
                break

        # product has been done!
        self.logger.info(f'Cost Time : {(datetime.now() - st).total_seconds():.1f} s')


class MidEval(BaseEval, ABC):
    """ Basic evaluate class to running evaluation product.
    Inspection products are obtained mainly through the function ``main``.

    Args:
        name: name of evaluation product.
        log_dir: directory of logger. Default: ``./logs``.
        max_counter: maximum number of counter to break evaluation. Default: ``1``.

    """

    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 res_columns: list,
                 method: str,
                 method_names: list,
                 save: str,
                 ) -> None:
        # Cannot use `super(MidEval, self).__init__()` !!!
        BaseEval.__init__(self, name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)
        self.res_columns = res_columns
        self.method = method
        self.method_names = method_names
        self.save = save

    def save_res(self,
                 tag_time: datetime,
                 lead_time: Optional[timedelta],
                 res: pd.DataFrame,
                 ) -> None:
        """ save evaluation product.

        Args:
            tag_time: target time of file.
            lead_time: lead time of file.
            res: result of evaluation product.
        """
        # Save evaluation product
        save_path = Path(PathCather.catch(time=tag_time, lead_time=lead_time, file=self.save))
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Fill NaN with fill_value
        res.fillna(value=self.data_cfg.fill_value, inplace=True)

        if save_path.exists():
            old_res = pd.read_json(str(save_path), orient='records', lines=True)
            res = pd.concat([old_res, res])
            if lead_time is None:
                res.loc[:, 'time'] = res.time.astype(str)
                res.drop_duplicates(subset=['time', 'type', 'area'], keep='last', inplace=True)
            else:
                res.loc[:, 'stime'] = res.stime.astype(str)
                res.loc[:, 'ftime'] = res.ftime.astype(str)
                res.drop_duplicates(subset=['stime', 'ftime', 'type', 'area'], keep='last', inplace=True)
            res.reset_index(drop=True, inplace=True)
        else:
            save_path.parent.mkdir(parents=True, exist_ok=True)
        res.to_json(save_path, orient='records', force_ascii=False, lines=True)
        if lead_time is None:
            self.logger.info(f"{tag_time} | Save Evaluation : {save_path}")
        else:
            self.logger.info(f"{tag_time} - {tag_time + lead_time} | Save Evaluation : {save_path}")

    @abstractmethod
    def _method_eval(self,
                     input: dict,
                     target: dict,
                     flag: Optional[ndarray],
                     res_tmp: dict,
                     ) -> None:
        raise NotImplementedError

    def _evaluate_all(self,
                      tag_time: datetime,
                      skip_bad: bool,
                      ):
        """ evaluation of all area."""

        # Read target data as truth.
        target = self.read_target(tag_time=tag_time, skip_bad=skip_bad)
        if not target['status']:
            return False

        for lead_time in self.data_cfg.time_list:
            if lead_time is None:
                report_time = tag_time
                # basic information of evaluation product
                res_columns = ['time', 'type', 'area', 'method']
                res_tmp = dict(time=tag_time.strftime('%Y%m%d%H%M'),
                               type=self.data_cfg.code,
                               area=self.data_cfg.area,
                               method=self.method,
                               )
            else:
                report_time = tag_time - lead_time
                # basic information of evaluation product
                res_columns = ['stime', 'ftime', 'type', 'area', 'method']
                res_tmp = dict(stime=report_time.strftime('%Y%m%d%H%M'),
                               ftime=tag_time.strftime('%Y%m%d%H%M'),
                               type=self.data_cfg.code,
                               area=self.data_cfg.area,
                               method=self.method,
                               )
            # Read input data as test.
            input = self.read_input(tag_time=report_time, lead_time=lead_time, skip_bad=skip_bad)
            if not input['status']:
                return False

            unified_shape(input, target=target, keys=self.data_cfg.keys)

            # initialize evaluation product
            res = pd.DataFrame(columns=res_columns + self.res_columns)

            # evaluation product, default without evaluating in different county.
            index = len(res)
            self._method_eval(input, target, flag=None, res_tmp=res_tmp)

            res.loc[index, :] = res_tmp
            # Save evaluation product
            self.save_res(tag_time=report_time, lead_time=lead_time, res=res)
        return True

    def _evaluate_area(self,
                       tag_time: datetime,
                       skip_bad: bool,
                       ):
        """ evaluation of each areas."""
        # Read target data as truth.
        target = self.read_target(tag_time=tag_time, skip_bad=skip_bad)
        if not target['status']:
            return False

        for lead_time in self.data_cfg.time_list:
            if lead_time is None:
                report_time = tag_time
                res_columns = ['time', 'type', 'area', 'method']
                # basic information of evaluation product
                base_info = dict(time=tag_time.strftime('%Y%m%d%H%M'),
                                 type=self.data_cfg.code,
                                 method=self.method,
                                 )
            else:
                report_time = tag_time - lead_time
                res_columns = ['stime', 'ftime', 'type', 'area', 'method']
                # basic information of evaluation product
                base_info = dict(stime=report_time.strftime('%Y%m%d%H%M'),
                                 ftime=tag_time.strftime('%Y%m%d%H%M'),
                                 type=self.data_cfg.code,
                                 method=self.method,
                                 )
            # Read input data as test.
            input = self.read_input(tag_time=report_time, lead_time=lead_time, skip_bad=skip_bad)
            if not input['status']:
                return False

            # initialize evaluation product
            res = pd.DataFrame(columns=res_columns + self.res_columns)
            if self.mode == 'Grid':
                unified_shape(input, target, target=self.data_cfg.border, keys=self.data_cfg.keys)
                # evaluation product, default without evaluating in different county.
                self.logger.debug('Grid |--> evaluation with areas.')
                for col in self.data_cfg.border['List'].itertuples():
                    if col.Code == -1:
                        # All area.
                        flag = np.where(self.data_cfg.border['Code'] != 0, True, False)
                        res_tmp = dict(area=self.data_cfg.area)
                    else:
                        # Special area with admin code.
                        flag = np.where(self.data_cfg.border['Code'] == col.Code, True, False)
                        res_tmp = dict(area=col.Name)
                    res_tmp.update(base_info)
                    index = len(res)
                    self._method_eval(input, target, flag=flag, res_tmp=res_tmp)
                    self.logger.debug(f'Each result |--> {res_tmp}')
                    res.loc[index, :] = res_tmp
            elif self.mode == 'Station':
                unified_shape(input, target=target, keys=self.data_cfg.keys)
                # evaluation product, default without evaluating in different county.
                for col in self.data_cfg.border['List'].itertuples():
                    if col.Code == -1:
                        # All area.
                        flag = np.ones_like(input[self.data_cfg.keys[0]]).astype(bool)
                        res_tmp = dict(area=self.data_cfg.area)
                    else:
                        # Special area with admin code.
                        flag = select_admin(target['dataframe'], col.Code)
                        res_tmp = dict(area=col.Name)
                    res_tmp.update(base_info)
                    index = len(res)
                    self._method_eval(input, target, flag=flag, res_tmp=res_tmp)
                    res.loc[index, :] = res_tmp
            else:
                raise ValueError(f'Expected mode in `Grid` or `Station`, but got {self.mode}.')
            # Save evaluation product
            self.save_res(tag_time=report_time, lead_time=lead_time, res=res)
        return True

    def evaluate(self,
                 tag_time: datetime,
                 skip_bad: bool = False,
                 ) -> bool:
        if self.data_cfg.border is None:
            self.logger.debug(f'Without border information for all. {self.data_cfg.border}')
            return self._evaluate_all(tag_time, skip_bad)
        else:
            self.logger.debug(f'With border information for areas. {self.data_cfg.border}')
            return self._evaluate_area(tag_time, skip_bad)


class ScoreEval(MidEval, ABC):
    """ Score Evaluation.

    Args:
        name:
        log_dir:
        max_counter:
        data_cfg:
        method_names:
        save:
        threshold:
        level:
        score_method: classification method for contingency table. Default: ``binary``.
            - ``binary``: for a threshold t1, larger than or equal to t1 is a positive and vice versa.
            - ``class``: for a threshold (t1, t2), within the threshold is considered a positive and vice versa.
            - ``level``: for a threshold (t1, t2), within the threshold is considered a positive, less than t1
                         is considered a negative. That is, without considering the case of larger than t2.

    """

    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 threshold: Optional[list] = None,
                 level: Optional[dict] = None,
                 score_method: str = 'binary',
                 ):
        _name = ['NA', 'NB', 'NC', 'ND'] + method_names
        if level is None:
            level = {'1': 'small', '2': 'mid', '3': 'big', '4': 'storm'}
        res_columns = [f'{b}_{a}' for a in level.values() for b in _name]
        super(ScoreEval, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                        res_columns=res_columns, method='TS',
                                        method_names=method_names, save=save)
        if threshold is None:
            threshold = Threshold.rain_1h
        self.threshold = threshold
        self.level = level
        self.score_method = score_method

    def _method_eval(self,
                     input: dict,
                     target: dict,
                     flag: Optional[ndarray],
                     res_tmp: dict,
                     ) -> None:
        for key in self.data_cfg.keys:
            flag = Score.drop_miss(input[key], target[key], flag=flag,
                                   amin=self.threshold[0], amax=self.threshold[-1])
            for lvl, lvl_name in self.level.items():
                # Note: threshold is tuple or number.
                #   - tuple, calculate score between in threshold, like (0.1, 5)
                #   - number, calculate score larger of threshold, like (0.1, ~)
                if self.score_method == 'binary':
                    table = Score.classify(target=target[key], input=input[key], flag=flag,
                                           threshold=self.threshold[int(lvl)])
                elif self.score_method == 'class':
                    threshold = (self.threshold[int(lvl)], self.threshold[int(lvl) + 1])
                    table = Score.classify(target=target[key], input=input[key], flag=flag, threshold=threshold)
                elif self.score_method == 'level':
                    threshold = (self.threshold[int(lvl)], self.threshold[int(lvl) + 1])
                    flag_tmp = flag & np.where((target[key] < threshold[1]) & (input[key] < threshold[1]), True, False)
                    table = Score.classify(target=target[key], input=input[key], flag=flag_tmp, threshold=threshold)
                else:
                    self.logger.error(f'Expected `score_method` in `binary`, `class` or `level`, '
                                      f'but got {self.score_method}!')
                    raise NotImplementedError(f'Expected `score_method` in `binary`, `class` or `level`, '
                                              f'but got {self.score_method}!')
                self.logger.debug(f'Score method: {self.score_method}')
                res_tmp.update({f'NA_{lvl_name}': table.tp,
                                f'NB_{lvl_name}': table.fp,
                                f'NC_{lvl_name}': table.fn,
                                f'ND_{lvl_name}': table.tn, })
                for _name in self.method_names:
                    res_tmp[f'{_name}_{lvl_name}'] = np.round(getattr(Score, _name.lower())(table),
                                                              self.data_cfg.precision)


class StatsEval(MidEval, ABC):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 threshold: Optional[list] = None,
                 ):
        res_columns = [f'{name}_{key}' for key in data_cfg.keys for name in method_names]
        super(StatsEval, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                        res_columns=res_columns, method='STATISTICS',
                                        method_names=method_names, save=save)
        if threshold is None:
            threshold = [-Inf, Inf]
        self.threshold = threshold

    def _method_eval(self,
                     input: dict,
                     target: dict,
                     flag: Optional[ndarray],
                     res_tmp: dict,
                     ) -> None:
        for key in self.data_cfg.keys:
            flag = Stats.drop_miss(input[key], target[key], flag=flag,
                                   amin=self.threshold[0], amax=self.threshold[-1])

            for _name in self.method_names:
                res_tmp[f'{_name}_{key}'] = np.round(getattr(Stats, _name.lower())(input[key],
                                                                                   target[key],
                                                                                   flag,
                                                                                   'mean'),
                                                     self.data_cfg.precision)


class SpaceEval(MidEval, ABC):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 threshold: Optional[list] = None,
                 min_point: int = 15,
                 ):
        assert method_names == ['SAL'], NotImplementedError('Space evaluation is only supported SAL yet, but got '
                                                            f'{method_names}!')
        res_columns = [f'{name}_{key}' for key in data_cfg.keys for name in ['S', 'A', 'L']]
        super(SpaceEval, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                        res_columns=res_columns, method='SAL',
                                        method_names=method_names, save=save)

        if threshold is None:
            threshold = [0.1, 999]
        self.threshold = threshold
        self.min_point = min_point

    def _method_eval(self,
                     input: dict,
                     target: dict,
                     flag: Optional[ndarray],
                     res_tmp: dict,
                     ) -> None:
        for key in self.data_cfg.keys:
            flag = Space.drop_miss(input[key], target[key], flag=flag,
                                   amin=self.threshold[0], amax=self.threshold[-1])
            tmp = Space.sal(input[key], target[key], flag=flag, threshold=self.threshold, min_point=self.min_point)

            for _name in ['S', 'A', 'L']:
                res_tmp[f'{_name}_{key}'] = np.round(tmp[_name], self.data_cfg.precision)

    def evaluate(self,
                 tag_time: datetime,
                 skip_bad: bool = False,
                 ) -> bool:
        # SAL cannot support evaluation for each areas.
        self.logger.debug('Space Evaluation with all areas.')
        return self._evaluate_all(tag_time, skip_bad)
