import os
import pandas as pd
from datetime import datetime
import time
import shutil

from django.core.management.base import BaseCommand
from trading.settings import BASE_HISTORICALLY_PATH, SHARE_PATH, REGION

from common.convert import convert_tz, parse_as_timestamp, timestamp_to_datetime, datetime_to_timestamp
from common.logger import log
from trading.models import Instruments
from trading.constants import DATE_TIME_FORMATE, RESEARCH_BOARTS, INDEX_MAP, DURATION, RESEARCH_FACTORS
from trading.manager import cal_factor_info, board_to_index_df

boards = ["INDEX", "SH", "MSB", "GEM", "SZ"]


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = int(time.time())
        self.prepare()
        for board in boards:
            base_hdf_path, factor_hdf_path = \
                BASE_HISTORICALLY_PATH + board + f"/base.h5", BASE_HISTORICALLY_PATH + board + f"/factor.h5"
            base_store, factor_store = pd.HDFStore(base_hdf_path), pd.HDFStore(factor_hdf_path)

            read_path = SHARE_PATH + board
            files = os.listdir(read_path)
            for file in files:
                try:
                    iuid, name, base_df = self.genetate_base(read_path, file, board)
                    if base_df.shape[0] == 0:
                        continue
                    base_store[iuid], factor_store[iuid] = base_df, self.generate_factor(base_df, name, board)  # 生成hdf文件
                except Exception as ex:
                    print(iuid, name)
                    print(ex)
                    print("xxxxxxxx")

            base_store.close()
            factor_store.close()
        duration_time = int(time.time()) - start_time
        print(f"{duration_time}s")


    def genetate_base(self, read_path, file, board):
        with open(f"{read_path}/{file}", "r", encoding="GB2312") as f:
            first_line = f.readline()
            iuid = first_line.split(" ")[0]
            tail = first_line.split(" ").index("日线")
            name = "".join(first_line.split(" ")[1:tail])
        # 读取数据, 并计算出涨跌幅
        tick_data = pd.read_csv(f"{read_path}/{file}", sep="\s+", encoding="gbk", header=1, skipfooter=1,
                                parse_dates=['日期'], index_col="日期", engine='python')
        size = tick_data.shape[0]
        if size == 0:
            return iuid, name, tick_data
        tick_data.index.name = name
        pct_change = tick_data["收盘"].pct_change()
        pct_change[0] = 0
        tick_data["涨跌幅"] = pct_change

        df_info = cal_factor_info(board, tick_data, flag=1)  # 年为单位,生成处还没相对指标
        avg_volume, avg_abs_volatility = df_info["avg_volume"], df_info["avg_abs_volatility"]
        tick_data["与年成交额的比率"] = tick_data["成交额"] / avg_volume
        if board == "INDEX":
            return iuid, name, tick_data

        # 计算相对指数涨跌幅
        relate_index_base_df, relate_index_factor_df = board_to_index_df(board)
        coefficient = 1/(relate_index_factor_df.loc["ONE_YEAR"]["avg_abs_volatility"]+1)*(1+avg_abs_volatility)
        series = relate_index_base_df["涨跌幅"].apply(self.eliment_coefficient, coefficient=coefficient)
        tick_data["去除指数涨跌幅"] = tick_data["涨跌幅"] - series
        return iuid, name, tick_data
        
    def prepare(self):
        shutil.rmtree(BASE_HISTORICALLY_PATH)
        os.mkdir(BASE_HISTORICALLY_PATH)
        for board in boards:
            board_dir = BASE_HISTORICALLY_PATH + board
            os.mkdir(board_dir)

    def generate_factor(self, base_df, name, board):
        data_lengths = [i for i in DURATION.NAME_TO_VALUE]
        factor_df = pd.DataFrame()
        factor_df.index.name = name
        for duration in data_lengths:
            res = cal_factor_info(board, base_df, duration_ts=DURATION.NAME_TO_VALUE[duration])
            series = pd.Series(res, name=duration)
            factor_df = factor_df.append(series)
        return factor_df

    def eliment_coefficient(self, value, coefficient):
        return value * coefficient