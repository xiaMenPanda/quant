import pandas as pd
import numpy as np

from trading.settings import BASE_HISTORICALLY_PATH, REGION
from datetime import datetime
from common.convert import convert_tz, parse_as_timestamp, timestamp_to_datetime, datetime_to_timestamp

from .constants import DATE_TIME_FORMATE, RESEARCH_BOARTS, INDEX_MAP, DURATION
from .models import Instruments


# 剔除INDEX对TICKER的影响的系数1的确认,(1/系数1)*波动率
def get_factor_index_to_ticker():
    factor_dict = {}
    for research_board in RESEARCH_BOARTS:
        volatilities = Instruments.objects.filter(board=research_board).values_list("base_volatility")
        volatilities = [i[0] for i in volatilities]
        index_iuid = INDEX_MAP[research_board]
        index_base_volatility = Instruments.objects.filter(iuid=index_iuid).first().base_volatility
        cal_board_base_volatility = sum(volatilities)/len(volatilities)
        facor_one = 100/(cal_board_base_volatility+100)  # 关键,单位换算1
        facor_one = float('%.2f' % facor_one)
        factor_dict[research_board] = (index_base_volatility, facor_one)
        print(f"{research_board} cal {facor_one}")
    return factor_dict


def absolute_value(value):
    return abs(value)


def cal_factor_info(board, df, duration_ts=DURATION.ONE_YEAR, flag=0):
    end_dt = convert_tz(datetime.now(), REGION)
    start_ts = datetime_to_timestamp(end_dt) - duration_ts
    start_dt = timestamp_to_datetime(start_ts, REGION)
    start_time = datetime.strftime(start_dt, DATE_TIME_FORMATE)
    end_time = datetime.strftime(end_dt, DATE_TIME_FORMATE)
    df = df[
        (pd.to_datetime(df.index) >= pd.to_datetime(start_time)) &
        (pd.to_datetime(df.index) <= pd.to_datetime(end_time))]
    cal_size = df.shape[0]
    avg_volume, avg_abs_volatility = df["成交额"].mean(), df["涨跌幅"].apply(absolute_value).mean()
    if flag:
        return {
            "cal_size": cal_size,
            "avg_volume": avg_volume,
            "avg_abs_volatility": avg_abs_volatility,
        }
    if cal_size == 0:
        cumulative_volatility = np.nan
    else:
        cumulative_volatility = df["涨跌幅"].sum() if board == "INDEX" else df["去除指数涨跌幅"].sum()

    return {
        "cal_size": cal_size,
        "avg_volume": avg_volume,
        "avg_abs_volatility": avg_abs_volatility,
        "cumulative_volatility": cumulative_volatility,
    }


def board_to_hdf(board):
    base_hdf_path, factor_hdf_path = \
        BASE_HISTORICALLY_PATH + board + f"/base.h5", BASE_HISTORICALLY_PATH + board + f"/factor.h5"
    base_store, factor_store = pd.HDFStore(base_hdf_path), pd.HDFStore(factor_hdf_path)
    return base_store, factor_store


def board_to_index_df(board):
    index = INDEX_MAP[board]
    base_hdf_path, factor_hdf_path = \
        BASE_HISTORICALLY_PATH + "INDEX" + f"/base.h5", BASE_HISTORICALLY_PATH + "INDEX" + f"/factor.h5"
    base_store, factor_store = pd.HDFStore(base_hdf_path), pd.HDFStore(factor_hdf_path)
    index_base_df, index_factor_df = base_store[index], factor_store[index]
    base_store.close()
    factor_store.close()
    return index_base_df, index_factor_df