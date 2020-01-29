import pandas as pd

from django.conf import settings
from datetime import datetime
from common.convert import convert_tz, parse_as_timestamp, timestamp_to_datetime

from .constants import DATE_TIME_FORMATE
from .models import Instruments

REGION ="CN"
START_DATE = "2019-01-01"
end_dt = convert_tz(datetime.now(), REGION)
END_DATE = datetime.strftime(end_dt, DATE_TIME_FORMATE)
def iuid_to_df(iuid, infos = None, durations=None, start_time=START_DATE, end_time=END_DATE):
    infos = ['日期', '涨跌幅', '成交额'] if not infos else ['日期', '涨跌幅', '成交额'].extend(infos)
    obj = Instruments.objects.filter(iuid=iuid).first()
    if not obj:
        raise ValueError(f"{iuid} is not exist")
    board = obj.board
    csv_name = f"{iuid}.csv"
    csv_path = f"{settings.BASE_DIR}/historically/{board}/{csv_name}"
    df = pd.read_csv(csv_path, sep=",")
    if durations:
        start_ts = parse_as_timestamp(end_time) - durations
        start_dt = timestamp_to_datetime(start_ts)
        start_time = datetime.strftime(start_dt, DATE_TIME_FORMATE)
    df = df[infos][
        (pd.to_datetime(df['日期']) >= pd.to_datetime(start_time)) &
        (pd.to_datetime(df['日期']) <= pd.to_datetime(end_time))]
    size = df.shape[0]
    if not size:
        return None
    result = {
        "size": size,
        "df": df
    }
    return result