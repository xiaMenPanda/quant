from django.core.management.base import BaseCommand
from django.conf import settings
from trading.models import Instruments
import os
import pandas as pd
from common.logger import log
import time

boards = ["SH", "MSB", "GEM", "SZ", "INDEX"]
base_path = "/mnt/hgfs/share_with_ub/"
class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = int(time.time())
        for board in boards:
            read_path = base_path + board
            files = os.listdir(read_path)
            for file in files:
                try:
                    with open(f"{read_path}/{file}", "r", encoding="GB2312") as f:
                        first_line = f.readline()
                        iuid = first_line.split(" ")[0]
                        tail = first_line.split(" ").index("日线")
                        name = "".join(first_line.split(" ")[1:tail])
                    tick_data = pd.read_csv(f"{read_path}/{file}", sep="\s+", encoding="gbk", header=1)[:-1]
                    if tick_data.isnull().any().values[0]:
                        print(f"{file}, 存在空数据")

                    size_in_file = tick_data.shape[0]
                    # 根据收盘价算出涨跌幅,并对成交额进行处理/10000
                    close_prices = list(tick_data["收盘"])
                    if tick_data.shape[0] != len(close_prices):
                        print(f"{file}, 收盘价计算涨跌幅有问题")
                    volatilies = [0]
                    for i in range(1, len(close_prices)):
                        rate = (close_prices[i]-close_prices[i-1])/close_prices[i-1]
                        rate = rate * 1000
                        rate = float('%.2f' % rate)
                        volatilies.append(rate)
                    tick_data["涨跌幅"] = volatilies
                    tick_data["成交额"] = tick_data["成交额"].map(self.volume_dividen)

                    # 计算绝对值平均波动率  计算平均交易额
                    avg_volatilty = sum([abs(i) for i in volatilies])/len(volatilies)
                    avg_volatilty = float('%.2f' % avg_volatilty)
                    avg_volume = sum(list(tick_data["成交额"]))/len(list(tick_data["成交额"]))
                    avg_volume = float('%.8f' % avg_volume)

                    avg_volume_rates = [float('%.2f' % (i/(avg_volume))) for i in list(tick_data["成交额"])]
                    tick_data["与年成交量比率"] = avg_volume_rates

                    # 保存到数据库中
                    params = {
                        "iuid": iuid,
                        "name": name,
                        "board": board,
                        "base_volatility": avg_volatilty,
                        "base_volume": avg_volume,
                        "size_in_file": size_in_file
                    }
                    _ = Instruments.objects.create(**params)
                    # 保存到文件中
                    csv_name = file.split(".")[0] + ".csv"
                    csv_name = csv_name[2:]
                    save_path = f"{settings.BASE_DIR}/historically/{board}/{csv_name}"
                    tick_data.to_csv(save_path, sep=",", header=True, index=True)
                except Exception as ex:
                    print(f"{iuid} failed because {ex}")
                    log.exception(f"{iuid} failed because {ex}")
                    if ex.args == 1062:
                        continue
                    following_path = f"{settings.BASE_DIR}/historically/data_man/lack_iuid"
                    with open(following_path, "a+") as f:
                        f.write(f"{iuid}  {ex}")
                        f.write("\n")
        duration_time = int(time.time()) - start_time
        print(f"{duration_time}s")

    def volume_dividen(self, value):
        return value/10000