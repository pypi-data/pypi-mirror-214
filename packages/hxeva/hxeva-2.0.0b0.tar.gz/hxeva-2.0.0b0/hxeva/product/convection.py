# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/6/1   17:33
----------------------------------
Author     : April
Contact    : fanglwh@foxmail.com
"""

__all__ = ['Convection', 'HeavyRain', 'Storm', 'WindStorm', 'Hail']

from abc import ABC
from datetime import datetime, timedelta
from pathlib import Path
import re
from typing import Optional, Callable, Union

import numpy as np
from numpy import ndarray, NaN
import pandas as pd
from pandas import DataFrame
from scipy.interpolate import griddata

from .base import MidEval, select_admin
from .config import Config
from .station import StationEval
from ..evaluate import Score, ContingencyTable
from ..meteorology import Threshold
from ..utils import PathCather, pool2d


class Convection(MidEval, StationEval, ABC):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 window_size: Union[int, tuple] = 20,
                 key: str = 'Convection',
                 ) -> None:
        res_columns = method_names + ['NA', 'NB', 'NC', 'ND']
        super(Convection, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                         res_columns=res_columns, method='TS', method_names=method_names, save=save)

        self.mode = StationEval.mode
        self.threshold = Threshold.pvalue
        self.window_size = window_size
        self.key = key

    def read_hourly(self,
                    tag_time: datetime,
                    file: dict,
                    func: Callable[[DataFrame], ndarray],
                    skip_bad: bool = False,
                    ) -> dict:
        """ Read hourly station data and transform factor into convection p-value by `func` method.

        Args:
            tag_time: target time of target file.
            file: hourly file.
            func: function for transforming target factor into convection p-value.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of hourly station data.
        """
        # Read target data as truth
        path = Path(PathCather.catch(time=self.transform_time(tag_time, timezone=file['timezone']),
                                     lead_time=None, file=file['file']))

        name = file['name']
        self.logger.debug(f'[{name}]| path: {path}')

        _columns = ['Station_Id_C', 'Admin_Code_CHN', 'Province', 'City', 'Cnty', 'Lat', 'Lon']
        res = dict(status=True)
        if path.exists():
            # load hourly station data
            data = pd.read_csv(path, sep='\t', low_memory=False, on_bad_lines='skip')
            flag = select_admin(data, self.data_cfg.admin_code)
            data = data.loc[flag, _columns + file['keys']]
            data.reset_index(drop=True, inplace=True)

            flag = func(data)
            data.loc[flag, self.key] = 99
            data.loc[~flag, self.key] = 0

            res.update({'dataframe': data,
                        'Lat': np.array(data.Lat),
                        'Lon': np.array(data.Lon),
                        'Time': np.array([tag_time for i in range(len(data))]),
                        self.key: np.array(data[self.key]),
                        })
            self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
        else:
            # Data is miss
            self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
            if skip_bad:
                # skip bad data, like missing.
                res[self.key] = np.array([NaN])
                tmp = pd.DataFrame(columns=_columns + file['keys'])
                tmp.loc[0, :] = -1
                res['dataframe'] = tmp
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
            else:
                res['status'] = False
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
        return res

    def read_adtd(self,
                  tag_time: datetime,
                  file: dict,
                  skip_bad: bool = False,
                  ):
        # Read tag_time ~ tag_time + 1h ADTD lightning data.
        paths, paths_time = [], []
        for delta in range(-30, 40, 10):
            tmp_time = tag_time + timedelta(minutes=delta)
            path = PathCather.catch(self.transform_time(tmp_time, timezone=file['timezone']),
                                    lead_time=None, file=file['file'])
            if Path(path).exists():
                paths.append(path)
                paths_time.append(tmp_time)

        name = file['name']
        _columns = ['Datetime', 'Lit_Prov', 'Lit_City', 'Lit_Cnty', 'Lat', 'Lon']
        res = dict(status=True)
        time_list = []
        if len(paths):
            data = pd.DataFrame()
            for path, ni in zip(paths, paths_time):
                self.logger.debug(f'[{name}]| path: {path}')
                tmp = pd.read_csv(path, sep='\t')
                data = pd.concat([data, tmp])
                time_list += [ni for i in range(len(tmp))]

            # radius 20km
            flag = np.where(
                (self.data_cfg.loc['lat1'] - 0.2 <= data.Lat) & (data.Lat <= self.data_cfg.loc['lat2'] + 0.2), True,
                False)
            flag &= np.where(
                (self.data_cfg.loc['lon1'] - 0.2 <= data.Lon) & (data.Lon <= self.data_cfg.loc['lon2'] + 0.2), True,
                False)
            data = data.loc[flag, _columns]
            data.reset_index(drop=True, inplace=True)
            if np.sum(flag):
                data.loc[:, self.key] = 99
                res.update({'dataframe': data,
                            'Lat': np.array(data.Lat),
                            'Lon': np.array(data.Lon),
                            'Time': np.array(time_list)[flag],
                            self.key: np.array(data[self.key]),
                            })
                self.logger.error(f'[{name}]| SUCCESS READ in time: {tag_time}!')
            else:
                res.update({'dataframe': data,
                            self.key: np.array([NaN])
                            })
                self.logger.error(f'[{name}]| SUCCESS READ BUT WITHOUT DATA in time: {tag_time}!')
        else:
            if skip_bad:
                tmp = pd.DataFrame(columns=_columns + [self.key])
                tmp.loc[0, :] = -1
                res.update({'dataframe': tmp,
                            self.key: np.array([NaN])
                            })
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
            else:
                res['status'] = False
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
        return res

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

            # pooled interpolated into target Lon & Lat
            pad_input = pool2d(input[self.key], window_size=self.window_size, stride=(1, 1), pad=True)
            if ('Lat' in target) and ('Lon' in target):
                input[f'{self.key}_pool'] = griddata((input['Lon'].ravel(), input['Lat'].ravel()),
                                                     pad_input.ravel(), (target['Lon'], target['Lat']),
                                                     method='nearest')

                # normal interpolated into target Lon & Lat
                input[self.key] = griddata((input['Lon'].ravel(), input['Lat'].ravel()),
                                           input[self.key].ravel(), (target['Lon'], target['Lat']), method='nearest')
                input['Lat'] = target['Lat']
                input['Lon'] = target['Lon']
            else:
                input[self.key] = np.full_like(target[self.key], NaN)

            # initialize evaluation product
            if lead_time is not None:
                input['report_time']: datetime = report_time
                res = pd.DataFrame(columns=res_columns + self.res_columns + ['T1', 'T2', 'T3'])
            else:
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
        return self._evaluate_all(tag_time, skip_bad)

    def _method_eval(self,
                     input: dict,
                     target: dict,
                     flag: Optional[ndarray],
                     res_tmp: dict,
                     ) -> None:

        flag = (~np.isnan(input[self.key])) & (~np.isnan(target[self.key]))
        if np.sum(flag):
            input_data, input_pool_data = input[self.key][flag], input[f'{self.key}_pool'][flag]
            target_data = target[self.key][flag]

            # classify with pooling data.
            target_pos = (50 <= target_data) & (target_data <= 100)  # positive target

            # update points, where target is positive, with maximum pooling.
            input_data[target_pos] = input_pool_data[target_pos]

            input_pos = (50 <= input_data) & (input_data <= 100)  # positive input

            input_neg = ~input_pos  # negative input
            target_neg = ~target_pos  # negative target
            table = ContingencyTable(tp=int(np.sum(target_pos & input_pos)),
                                     fp=int(np.sum(target_neg & input_pos)),
                                     fn=int(np.sum(target_pos & input_neg)),
                                     tn=int(np.sum(target_neg & input_neg)),
                                     )

            # calculate early warning time.
            if 'report_time' in input:
                delta = np.array([(ti - input['report_time']).total_seconds() for ti in target['Time']])
                if np.sum(target_pos & input_pos):
                    res_tmp['t1'] = np.mean(delta[target_pos & input_pos])
                else:
                    res_tmp['t1'] = -1
                if np.sum(target_pos):
                    res_tmp['t2'] = np.mean(delta[target_pos])
                else:
                    res_tmp['t2'] = -1
                if np.sum(~(target_neg & input_neg)):
                    res_tmp['t3'] = np.mean(delta[~(target_neg & input_neg)])
                else:
                    res_tmp['t3'] = -1
        else:
            table = ContingencyTable(tp=-1, fp=-1, fn=-1, tn=-1)

        res_tmp.update({'NA': table.tp, 'NB': table.fp, 'NC': table.fn, 'ND': table.tn, })

        # calculate score
        for _name in self.method_names:
            res_tmp[f'{_name}'] = np.round(getattr(Score, _name.lower())(table), self.data_cfg.precision)


class HeavyRain(Convection):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 window_size: Union[int, tuple] = 20,
                 heavy_threshold: Optional[int] = None,
                 ) -> None:
        super(HeavyRain, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                        method_names=method_names, save=save, window_size=window_size, key='HeavyRain')
        self.mode = StationEval.mode

        if heavy_threshold is None:
            heavy_threshold = 20

        self.heavy_threshold = heavy_threshold

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        heavy_threshold = self.heavy_threshold

        def _func(data: DataFrame) -> ndarray:
            flag = data.PRE_1h >= heavy_threshold
            return flag

        return self.read_hourly(tag_time=tag_time, file=self.data_cfg.target_file,
                                func=_func, skip_bad=skip_bad)


class Storm(Convection):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 window_size: Union[int, tuple] = 20,
                 ) -> None:
        super(Storm, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                    method_names=method_names, save=save, window_size=window_size, key='Storm')
        self.mode = StationEval.mode

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        return self.read_adtd(tag_time, file=self.data_cfg.target_file, skip_bad=skip_bad)


class WindStorm(Convection):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 window_size: Union[int, tuple] = 20,
                 wind_threshold: Optional[dict] = None,
                 ) -> None:
        super(WindStorm, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                        method_names=method_names, save=save, window_size=window_size, key='Windstorm')
        self.mode = StationEval.mode

        # threshold of Storm, default: max wind speed >= 17.2 m/s  or average wind speed >= 10.8 m/s
        if wind_threshold is None:
            wind_threshold = dict(max=17.2, avg=10.8)
        self.wind_threshold = wind_threshold

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        ws_max, ws_avg = self.wind_threshold['max'], self.wind_threshold['avg']

        def _func(data: DataFrame) -> ndarray:
            _flag = (ws_max <= data.WIN_S_Max) & (data.WIN_S_Max <= 100)
            _flag &= (ws_avg <= data.WIN_S_Avg_2mi) & (data.WIN_S_Avg_2mi <= 100)
            return _flag

        # read hourly station
        station = self.read_hourly(tag_time, file=self.data_cfg.target_file,
                                   func=_func, skip_bad=skip_bad)

        # read lightning data.
        if ('Lat' in station) and ('Lon' in station):
            adtd = self.read_adtd(tag_time, file=self.data_cfg.target_file['adtd_file'],
                                  skip_bad=skip_bad)
            if ('Lat' in adtd) and ('Lon' in adtd):
                m, n = len(station[self.key]), len(adtd[self.key])
                _lon, _lat = np.zeros((m, n)), np.zeros((m, n))
                for ni in range(n):
                    _lon[:, ni] = station['Lon'] - adtd['Lon'][ni]
                    _lat[:, ni] = station['Lat'] - adtd['Lat'][ni]
                dis = np.power(np.power(_lon, 2) + np.power(_lat, 2), 0.5)
                flag = np.sum(dis <= 0.2, axis=1) > 0
            else:
                flag = np.zeros_like(station[self.key]).astype(bool)

            station['dataframe'].loc[~flag, self.key] = 0
            station[self.key] = np.array(station['dataframe'][self.key])
            return station
        else:
            return station


class Hail(Convection, ABC):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 window_size: Union[int, tuple] = 20,
                 ) -> None:
        super(Hail, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                   method_names=method_names, save=save, window_size=window_size, key='Hail')
        self.mode = StationEval.mode

    def read_target(self,
                    tag_time: datetime,
                    skip_bad: bool = False,
                    ) -> dict:
        """ Read daily station data and transform factor into convection p-value by `func` method.

        Args:
            tag_time: target time of target file.
            skip_bad: skip bad data, like data missing. Default: ``False``.

        Returns:
            dict:
                - dictionary of hourly station data.
        """
        # Read target data as truth
        path = Path(PathCather.catch(time=self.transform_time(tag_time, timezone=self.data_cfg.target_file['timezone']),
                                     lead_time=None, file=self.data_cfg.target_file['file']))

        name = self.data_cfg.target_file['name']
        self.logger.debug(f'[{name}]| path: {path}')

        _columns = ['Station_Id_C', 'Admin_Code_CHN', 'Province', 'City', 'Cnty', 'Lat', 'Lon', 'Datetime']
        res = dict(status=True)
        if path.exists():
            # load hourly station data
            data: DataFrame = pd.read_csv(path, sep='\t', low_memory=False, on_bad_lines='skip')
            flag = select_admin(data, self.data_cfg.admin_code)
            data = data.loc[flag, _columns + self.data_cfg.target_file['keys']]
            data.reset_index(drop=True, inplace=True)

            # select hail marked as True
            data = data.loc[~data.HAIL_OTime.isin([999999, '999999', '999998']), :]

            new_data = pd.DataFrame(columns=_columns)

            if np.sum(data):
                index = len(new_data)
                for col in data.itertuples():
                    date_time = datetime.strptime(getattr(col, 'Datetime'), '%Y-%m-%d %H:%M:%S')  # CST
                    for hail_time in re.sub(r'[^0-9]', '/', str(getattr(col, 'HAIL_OTime'))).split("/"):
                        try:
                            # Hail Time
                            if len(hail_time) == 0:
                                continue
                            elif len(hail_time) <= 4:
                                # %H%M: 836 --> 08:36 | 1424 --> 14:24
                                start_time = date_time + timedelta(
                                    minutes=int(hail_time[:-2]) * 60 + int(hail_time[-2:]))
                                end_time = start_time
                            elif len(hail_time) == 7:
                                # %H%M - %H%M: 9361010 --> 09:36 - 10:10
                                start_time = date_time + timedelta(
                                    minutes=int(hail_time[:1]) * 60 + int(hail_time[1:3]))
                                end_time = date_time + timedelta(
                                    minutes=int(hail_time[3:-2]) * 60 + int(hail_time[-2:]))
                            elif len(hail_time) == 8:
                                # %H%M - %H%M: 15281529 --> 15:28 - 15:29
                                start_time = date_time + timedelta(
                                    minutes=int(hail_time[:2]) * 60 + int(hail_time[2:4]))
                                end_time = date_time + timedelta(minutes=int(hail_time[4:6]) * 60 + int(hail_time[6:8]))
                            else:
                                # self.logger.error(f'{tag_time} --->| Cannot read hail time: {hail_time}!!')
                                # self.logger.error(f'Daily Station File: {path}')
                                print(hail_time)
                                raise NotImplementedError
                            # Basic Information
                            for _c in _columns:
                                new_data.loc[index, _c] = getattr(col, _c)
                            # Time window for hail is: 30 min before ~ 30 min after  | CST -> UTC
                            new_data.loc[index, 'stime'] = start_time - timedelta(minutes=30) - timedelta(hours=8)
                            new_data.loc[index, 'etime'] = end_time + timedelta(minutes=30) - timedelta(hours=8)
                            new_data.loc[index, self.key] = 99
                            index += 1
                        except Exception as e:
                            # self.logger.warning(e.__str__())
                            print(e.__str__())
                            continue

            res.update({'dataframe': new_data,
                        'Lat': np.array(new_data.Lat),
                        'Lon': np.array(new_data.Lon),
                        'Time': np.array(new_data.stime),
                        self.key: np.array(new_data[self.key]),
                        })
            self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
        else:
            # Data is miss
            self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
            if skip_bad:
                # skip bad data, like missing.
                res[self.key] = np.array([NaN])
                tmp = pd.DataFrame(columns=_columns + self.data_cfg.target_file['keys'])
                tmp.loc[0, :] = -1
                res['dataframe'] = tmp
                self.logger.error(f'[{name}]| MISS DATA BUT CONTINUE: {tag_time}!')
            else:
                res['status'] = False
                self.logger.error(f'[{name}]| MISS DATA in time: {tag_time}!')
        return res

    def _evaluate_all(self,
                      tag_time: datetime,
                      skip_bad: bool,
                      ):
        """ evaluation of all area."""

        # Read target data as truth.
        target = self.read_target(tag_time=tag_time, skip_bad=skip_bad)
        if not target['status']:
            return False
        # evaluation of hail is daily, 0H ~ 24H(UTC)
        for delta_hour in range(24):
            tag_time -= timedelta(hours=1)
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

                # pooled interpolated into target Lon & Lat
                pad_input = pool2d(input[self.key], window_size=self.window_size, stride=(1, 1), pad=True)
                if ('Lat' in target) and ('Lon' in target):
                    input[f'{self.key}_pool'] = griddata((input['Lon'].ravel(), input['Lat'].ravel()),
                                                         pad_input.ravel(), (target['Lon'], target['Lat']),
                                                         method='nearest')

                    # normal interpolated into target Lon & Lat
                    input[self.key] = griddata((input['Lon'].ravel(), input['Lat'].ravel()),
                                               input[self.key].ravel(), (target['Lon'], target['Lat']),
                                               method='nearest')
                    input['Lat'] = target['Lat']
                    input['Lon'] = target['Lon']
                else:
                    input[self.key] = np.full_like(target[self.key], NaN)

                # initialize evaluation product
                if lead_time is not None:
                    input['report_time']: datetime = report_time
                    res = pd.DataFrame(columns=res_columns + self.res_columns + ['T1', 'T2', 'T3'])
                else:
                    res = pd.DataFrame(columns=res_columns + self.res_columns)

                # evaluation product, default without evaluating in different county.
                index = len(res)
                if len(target['dataframe']):
                    flag = (target['dataframe'].stime <= tag_time) & (tag_time <= target['dataframe'].etime)
                else:
                    flag = np.full_like(target[self.key], NaN)
                self._method_eval(input, target, flag=flag, res_tmp=res_tmp)

                res.loc[index, :] = res_tmp
                # Save evaluation product
                self.save_res(tag_time=report_time, lead_time=lead_time, res=res)
        return True
