# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/26   15:47
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['PathCather']

from datetime import datetime, timedelta
import glob
from pathlib import Path
import re
from typing import Optional


class PathCather(object):

    @classmethod
    def catch(cls,
              time: datetime,
              lead_time: Optional[timedelta],
              file: str,
              ) -> str:
        """ Catch the path within time, lead time and file rule.

        Args:
            time: The time or report time of the file
            lead_time: None of the observation file.However, it is lead time of the forecast file.
            file: The rule of the file within time format.

        Returns:
            The path of file

        Exampls:
            >>> from datetime import datetime, timedelta
            >>> tag_time = datetime(year=2022, month=7, day=2, hour=4)
            >>> file1 = "/mnt/PRESKY/data/cmadata/NAFP/CMPAS_GRIB/%Y/%Y%m/%Y%m%d/*%Y%m%d%H.GRB2"
            >>> file2 = "~/product/FCST/SZW_1000M/F_RADA_FCST_03H_DL/%Y%m%d/F_RADA_FCST_03H_DL_SZW_1000M_%Y%m%d%H%M_%Y%m%d%H%M.nc"
            >>>path1 = PathCather.catch(time=tag_time + timedelta(hours=1), lead_time=None, file=file1)
            >>> path2 = PathCather.catch(time=tag_time, lead_time=timedelta(hours=1), file=file2)

        """
        if file.count('*') > 0:
            # fuzzy matching
            if file.count('%Y') + file.count('%m') + file.count('%d') > 0:
                assert lead_time is None, TypeError(f'{datetime.now()}\n ftime is exists!')
                file = time.strftime(file)
            path = glob.glob(file)
            # keep file size large than 0.
            if len(path) > 1:
                path = [Path(p).stat().st_size > 0 for p in path]
            if len(path) > 0:
                # sort paths with file time.
                path = sorted(path, key=lambda x: Path(x).stat().st_ctime, reverse=True)
                # return the latest file.
                path = path[0]
            else:
                path = file
        else:
            # precise Matching
            num = re.findall('{:0(\d)d}', file)
            if len(num) == 1 and isinstance(lead_time, timedelta):
                if num[0] in ['3']:
                    file = file.format(int(lead_time.total_seconds() // 60))
                elif num[0] in ['2']:
                    # path to a file with a pattern file name containing the number of hours in the forecast
                    file = file.format(int(lead_time.total_seconds() // 3600))
                else:
                    pass
            path = cls.merge_file(time, lead_time=lead_time, file=file)
        return path

    @classmethod
    def merge_file(cls,
                   time: datetime,
                   lead_time: Optional[timedelta],
                   file: str
                   ) -> str:
        """Merge file path.

        While the file is observation, it will return the file. However, the file is forecast,it will return the file
        merge the report time and forecast time.

        Args:
            time: The time or report time of the file
            lead_time: None of the observation file.However, it is lead time of the forecast file.
            file: The rule of the file within time format.

        Returns:
            The file.
        """
        if lead_time is None:
            # If the lead_time is `None`, the data is live
            return time.strftime(file)
        else:
            # If the lead_time is not `None`, the `time` is considered to be the report time
            file_split_1 = time.strftime("_".join(file.split("_")[:-1]))
            file_split_2 = (time + lead_time).strftime(file.split("_")[-1])
            file = file_split_1 + "_" + file_split_2
            return file
