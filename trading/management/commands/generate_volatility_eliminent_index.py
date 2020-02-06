import os
import pandas as pd
import time

from django.core.management.base import BaseCommand
from django.conf import settings
from common.logger import log

from trading.models import Instruments
from trading.manager import get_factor_index_to_ticker, iuid_to_df_info
from trading.constants import RESEARCH_BOARTS, INDEX_MAP


class Command(BaseCommand):
    def handle(self, *args, **options):
        dict_factor = get_factor_index_to_ticker()
        for research_board in RESEARCH_BOARTS:
            iuids = Instruments.objects.filter(board=research_board).values_list("iuid")
            iuids = [i[0] for i in iuids]
            index_iuid = INDEX_MAP[research_board]
            index_info = iuid_to_df_info(index_iuid)
            index_df = index_info["df"]
            for iuid in iuids:
                iuid_info = iuid_to_df_info(iuid)
                iuid_df = iuid_info["df"]
                data_merge = pd.merge(iuid_df, index_df, on="日期", how="left")
                obj = Instruments.objects.filter(iuid=iuid).first()
                factor_one, facter_two = dict_factor[obj.board][1], (obj.base_volatility+100)/100
                facter_all = factor_one * facter_two
                facter_all = float('%.2f' % facter_all)
                iuid_df["去除指数涨跌幅"] = data_merge["涨跌幅_x"] \
                                     - data_merge["涨跌幅_y"].apply(self.cal_factor, facter_all=facter_all)
                iuid_df["去除指数涨跌幅"] = iuid_df["去除指数涨跌幅"].map(self.handle_float)
                iuid_df.to_csv(iuid_info["csv_path"], sep=",", header=True, index=True)
                print("xxx")

    def cal_factor(self, value, **kwargs):
        value = value * kwargs["facter_all"]
        value = float('%.2f' % value)
        return value

    def handle_float(self, value):
        value = float('%.2f' % value)
        return value