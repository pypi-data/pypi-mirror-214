# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/25   15:28
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['Micaps',
           'SWAN',
           'SWANPRESta', 'SWANFactorSta',
           'SWANPREGrid', 'SWANFactorGrid',
           'SWANFactorGridART', 'SWANPREGridART', 'SWANSpaceGridART']

from abc import ABC, abstractmethod
import bz2
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import struct
from typing import Optional

import numpy as np
from numpy import NaN
import xarray as xr

from .art1km import PREGridART, FactorGridART, SpaceGridART
from .config import Config
from .base import BaseEval
from .grid import PREGrid, FactorGrid
from .station import PRESta, FactorSta
from ..utils import PathCather


@dataclass
class HeaderBlock(ABC):
    @classmethod
    @abstractmethod
    def read(cls, fp, byte_order='<'):
        raise NotImplementedError


@dataclass
class Micaps131Header(HeaderBlock):
    file_format: bytes  # 12s ; diamond 131
    file_info: bytes  # 38s ; 数据说明
    file_flag: bytes  # 8s  ; 文件标志; 'swan'
    file_vers: bytes  # 8s  ; 数据版本号, '1.0', 目前为2.0
    year: int  # H   ; 年
    month: int  # H   ; 月
    day: int  # H   ; 日
    hour: int  # H   ; 时
    minute: int  # H   ; 分
    interval: int  # H   ; 时间分辨率; 分钟
    x_num_grids: int  # H   ; 网格列数
    y_num_grids: int  # H   ; 网格行数
    z_num_grids: int  # H   ; 网格垂直层数; 目前为1
    radar_count: int  # i   ; 拼图雷达数
    start_lon: float  # f   ; 网格开始经度(左上角)
    start_lat: float  # f   ; 网格开始纬度(左上角)
    center_lon: float  # f   ; 网格中心经度
    center_lat: float  # f   ; 网格中心纬度
    x_reso: float  # f   ; 经度方向分辨率
    y_reso: float  # f   ; 纬度方向分辨率
    z_high_grids: float  # 40f ; 垂直方向的高度(单位km)数目根据z_num_grids而得(最大40层)
    radar_station_name: bytes  # 20s ; 相关站点名称
    radar_lon: float  # 20f ; 相关站点经度
    radar_lat: float  # 20f ; 相关站点纬度
    radar_alti: float  # 20f ; 相关站点海拔高度
    mosaic_flag: bytes  # 20B ; 该相关站点是否包含在本次拼图中
    # === 数据类型定义, 版本=1.5
    data_type: int  # h   ; 变量类型; 0=unsigned char; 1=char; 2=unsigned short; 3=short
    # === 每一层的向量数, 版本=2.0
    data_level: int  # h   ; 垂直层向量; 每一层向量数
    data_offset: float  # f   ; 偏移
    data_scale: float  # f   ; 缩放
    reserve: bytes  # 160s; 保留

    @classmethod
    def read(cls, fp, byte_order='<'):
        result = list(struct.unpack(f'{byte_order}12s38s8s8s9Hi6f', fp.read(112)))
        result.append(list(struct.unpack(f'{byte_order}40f', fp.read(160))))
        result.append(list(struct.unpack(f'{byte_order}320s', fp.read(320))))
        result.append(list(struct.unpack(f'{byte_order}20f', fp.read(80))))
        result.append(list(struct.unpack(f'{byte_order}20f', fp.read(80))))
        result.append(list(struct.unpack(f'{byte_order}20f', fp.read(80))))
        result.append(list(struct.unpack(f'{byte_order}20B', fp.read(20))))
        result = result + list(struct.unpack(f'{byte_order}2h2f160s', fp.read(172)))
        for i in [0, 1, 2, 3, -1]:
            result[i] = result[i].rstrip(b'\x00')
        return cls(*result)


class Micaps(object):
    @staticmethod
    def _open(file: str):
        suffix = file.split('.')[-1]
        if suffix in ['bz2', 'BZ2']:
            return bz2.open(file, 'rb')
        elif suffix in ['bin']:
            return open(file, 'rb')
        else:
            raise ValueError('file suffix')

    @classmethod
    def read_micaps_131(cls, file: str):
        type_format = {
            0: {'type': 'B', 'size': 1},
            1: {'type': 'b', 'size': 1},
            2: {'type': 'H', 'size': 2},
            3: {'type': 'h', 'size': 2},
        }

        with cls._open(file) as fp:
            header = Micaps131Header.read(fp)

            if header.data_type not in type_format.keys():
                return None

            lat = np.linspace(header.start_lat, header.start_lat - (header.y_num_grids * header.y_reso),
                              header.y_num_grids)
            lon = np.linspace(header.start_lon, header.start_lon + (header.x_num_grids * header.x_reso),
                              header.x_num_grids)

            data_len = header.x_num_grids * header.y_num_grids * header.z_num_grids
            var = np.frombuffer(
                fp.read(data_len * type_format[header.data_type]['size']),
                dtype=f"{data_len}{type_format[header.data_type]['type']}"
            )
            if header.z_num_grids != 1:
                var = var.reshape((header.z_num_grids, header.y_num_grids, header.x_num_grids))
            else:
                var = var.reshape((header.y_num_grids, header.x_num_grids))

            header.data_offset = 0 if header.data_offset == 0 else np.float32(header.data_offset)
            header.data_scale = 1 if header.data_scale == 1 else np.float32(header.data_scale)
            var = var * header.data_scale + header.data_offset

            lat = lat[::-1]
            if header.z_num_grids != 1:
                var = var[:, ::-1, :]
            else:
                var = var[::-1, :]

            result = xr.Dataset()
            result.attrs = dict(
                time=datetime(header.year, header.month, header.day, header.hour, header.minute),
                file_flag=header.file_flag,
                file_vers=header.file_vers,
                radar_count=header.radar_count,
            )

            result.coords['latitude'] = lat
            result.coords['longitude'] = lon

            result['latitude'] = (('latitude',), lat)
            result['latitude'].attrs = dict(long_name='latitude', units='degrees_south')
            result['longitude'] = (('longitude',), lon)
            result['longitude'].attrs = dict(long_name='longitude', units='degrees_west')

            if header.z_num_grids != 1:
                result.coords['altitude'] = header.z_high_grids
                result['altitude'] = (('altitude',), header.z_high_grids)
                result['altitude'].attrs = dict(long_name='altitude', units='km')
                result['var'] = (('altitude', 'latitude', 'longitude'), var)
            else:
                result['var'] = (('latitude', 'longitude'), var)

            return result


class SWAN(BaseEval, ABC):
    def __init__(self,
                 data_cfg: Config,
                 name: str = 'SWAN',
                 log_dir: str = './logs',
                 max_counter: int = 1,
                 ):
        super(SWAN, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg)

    def read_swan(self,
                  tag_time: datetime,
                  lead_time: timedelta,
                  skip_bad: bool = False,
                  ) -> dict:
        # Read input data as test  --> Product QPF
        file = self.data_cfg.input_file['file'].format(int(lead_time.total_seconds() // 60))
        path = Path(PathCather.catch(time=self.transform_time(tag_time, timezone=self.data_cfg.input_file['timezone']),
                                     lead_time=None, file=file))
        name = self.data_cfg.input_file['name']
        self.logger.debug(f'[{name}] | path: {path}')

        res = dict(status=True)
        if path.exists():
            tmp = Micaps.read_micaps_131(str(path))
            nlat = np.where(
                (self.data_cfg.loc['lat1'] <= tmp.latitude.data) & (tmp.latitude.data <= self.data_cfg.loc['lat2']))
            nlon = np.where(
                (self.data_cfg.loc['lon1'] <= tmp.longitude.data) & (tmp.longitude.data <= self.data_cfg.loc['lon2']))
            lon, lat = np.meshgrid(tmp.longitude.data[nlon], tmp.latitude.data[nlat])
            tmp = tmp.sel(latitude=slice(self.data_cfg.loc['lat1'], self.data_cfg.loc['lat2']),
                          longitude=slice(self.data_cfg.loc['lon1'], self.data_cfg.loc['lon2']))
            res.update({'dataset': tmp,
                    'Lat': lat,
                    'Lon': lon,
                    self.data_cfg.keys[0]: tmp.get('var').data,
                    })
            self.logger.info(f'[{name}]| SUCCESS READ in time: {tag_time}!')
        else:
            if skip_bad:
                # skip bad data, like missing.
                res['Lon'], res['Lat'] = np.meshgrid(np.linspace(self.data_cfg.loc['lon1'],
                                                                   self.data_cfg.loc['lon2'],
                                                                   self.data_cfg.input_file['shape'][1]),
                                                       np.linspace(self.data_cfg.loc['lat1'],
                                                                   self.data_cfg.loc['lat2'],
                                                                   self.data_cfg.input_file['shape'][0]))
                for key in self.data_cfg.input_file['keys']:
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


class SWANPRESta(PRESta, SWAN):
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
        super(SWANPRESta, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                         method_names=method_names, save=save,
                                         threshold=threshold, level=level, score_method=score_method)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANPRESta, self).read_swan(tag_time, lead_time, skip_bad)


class SWANFactorSta(FactorSta, SWAN):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 max_counter: int = 1,
                 threshold: Optional[list] = None,
                 ):
        super(SWANFactorSta, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                            method_names=method_names, save=save,
                                            threshold=threshold)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANFactorSta, self).read_swan(tag_time, lead_time, skip_bad)


class SWANPREGrid(PREGrid, SWAN):
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
        super(SWANPREGrid, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                          method_names=method_names, save=save,
                                          threshold=threshold, level=level, score_method=score_method)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANPREGrid, self).read_swan(tag_time, lead_time, skip_bad)


class SWANFactorGrid(FactorGrid, SWAN):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 threshold: Optional[list] = None,
                 ):
        super(SWANFactorGrid, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                             method_names=method_names, save=save,
                                             threshold=threshold)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANFactorGrid, self).read_swan(tag_time, lead_time, skip_bad)


class SWANPREGridART(PREGridART, SWAN):
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
        super(SWANPREGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                             method_names=method_names, save=save, threshold=threshold, level=level,
                                             score_method=score_method)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANPREGridART, self).read_swan(tag_time, lead_time, skip_bad)


class SWANFactorGridART(FactorGridART, SWAN):
    def __init__(self,
                 name: str,
                 log_dir: str,
                 max_counter: int,
                 data_cfg: Config,
                 method_names: list,
                 save: str,
                 threshold: Optional[list] = None,
                 ):
        super(SWANFactorGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                                method_names=method_names, save=save, threshold=threshold)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANFactorGridART, self).read_swan(tag_time, lead_time, skip_bad)


class SWANSpaceGridART(SpaceGridART, SWAN):
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
        super(SWANSpaceGridART, self).__init__(name=name, log_dir=log_dir, max_counter=max_counter, data_cfg=data_cfg,
                                               method_names=method_names, save=save, threshold=threshold,
                                               min_point=min_point)

    def read_input(self,
                   tag_time: datetime,
                   lead_time: Optional[timedelta],
                   skip_bad: bool = False,
                   ) -> dict:
        return super(SWANSpaceGridART, self).read_swan(tag_time, lead_time, skip_bad)
