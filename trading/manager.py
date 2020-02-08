import pandas as pd
import numpy as np

from trading.settings import BASE_HISTORICALLY_PATH, REGION, SHARE_PATH, TRADE_DATES
from datetime import datetime
from common.convert import convert_tz, parse_as_timestamp, timestamp_to_datetime, datetime_to_timestamp

from .constants import DATE_TIME_FORMATE, RESEARCH_BOARTS, INDEX_MAP, DURATION
from .models import Instruments


def absolute_value(value):
    return abs(value)


def cal_factor_info(board, df, trade_dates_before=DURATION.ONE_YEAR, trade_dates_before_stop=-1, flag=0):
    start_time = TRADE_DATES[-trade_dates_before]
    end_time = TRADE_DATES[trade_dates_before_stop]
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


def get_factor_mysql(factor_df):
    factor_mysql_params = {}
    cal_size_series = factor_df["cal_size"]
    cum_volatility_series = factor_df["cumulative_volatility"]
    avg_volume_series = factor_df["avg_volume"]
    avg_abs_volatility_series = factor_df["avg_abs_volatility"]
    
    # 平均成交量， 取4个比值参数参数
    factor_mysql_params["base_volume"] = avg_volume_series.ONE_YEAR
    factor_mysql_params[
        "avg_volume_three_days_div_two_weeks"] = avg_volume_series.THREE_DAYS / avg_volume_series.TWO_WEEKS
    factor_mysql_params[
        "avg_volume_one_week_div_one_month"] = avg_volume_series.ONE_WEEK / avg_volume_series.ONE_MONTH
    factor_mysql_params[
        "avg_volume_two_weeks_div_two_months"] = avg_volume_series.TWO_WEEKS / avg_volume_series.TWO_MONTHS
    factor_mysql_params[
        "avg_volume_one_month_div_one_year"] = avg_volume_series.ONE_MONTH / avg_volume_series.ONE_YEAR

    # 平均价格变化大小， 取4个比值参数参数
    factor_mysql_params["base_volatility"] = avg_abs_volatility_series.ONE_YEAR
    factor_mysql_params[
        "avg_abs_volatility_three_days_div_two_weeks"] = avg_abs_volatility_series.THREE_DAYS / avg_abs_volatility_series.TWO_WEEKS
    factor_mysql_params[
        "avg_abs_volatility_one_week_div_one_month"] = avg_abs_volatility_series.ONE_WEEK / avg_abs_volatility_series.ONE_MONTH
    factor_mysql_params[
        "avg_abs_volatility_two_weeks_div_two_months"] = avg_abs_volatility_series.TWO_WEEKS / avg_abs_volatility_series.TWO_MONTHS
    factor_mysql_params[
        "avg_abs_volatility_one_month_div_one_year"] = avg_abs_volatility_series.ONE_MONTH / avg_abs_volatility_series.ONE_YEAR

    # 最新一天是否还在
    factor_mysql_params["cal_size_on_day"] = cal_size_series.ONE_DAY
    factor_mysql_params["cal_size_two_days"] = cal_size_series.TWO_DAYS
    factor_mysql_params["cal_size_three_days"] = cal_size_series.THREE_DAYS
    factor_mysql_params["cal_size_one_week"] = cal_size_series.ONE_WEEK
    factor_mysql_params["cal_size_two_weeks"] = cal_size_series.TWO_WEEKS
    factor_mysql_params["cal_size_one_month"] = cal_size_series.ONE_MONTH
    factor_mysql_params["cal_size_two_months"] = cal_size_series.TWO_MONTHS
    factor_mysql_params["cal_size_two_months"] = cal_size_series.TWO_MONTHS
    factor_mysql_params["cal_size_three_months"] = cal_size_series.THREE_MONTHS
    factor_mysql_params["cal_size_six_months"] = cal_size_series.SIX_MONTHS

    # 累计涨幅参数
    factor_mysql_params["cum_volatility_one_week"] = cum_volatility_series.ONE_WEEK
    factor_mysql_params["cum_volatility_two_weeks"] = cum_volatility_series.TWO_WEEKS
    factor_mysql_params["cum_volatility_one_month"] = cum_volatility_series.ONE_MONTH
    factor_mysql_params["cum_volatility_two_months"] = cum_volatility_series.TWO_MONTHS
    factor_mysql_params["cum_volatility_two_months"] = cum_volatility_series.TWO_MONTHS
    factor_mysql_params["cum_volatility_three_months"] = cum_volatility_series.THREE_MONTHS
    factor_mysql_params["cum_volatility_six_months"] = cum_volatility_series.SIX_MONTHS

    for key, value in factor_mysql_params.items():
        factor_mysql_params[key] = float('%.4f' % value)

    return factor_mysql_params