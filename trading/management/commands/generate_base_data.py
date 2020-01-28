from django.core.management.base import BaseCommand
import os
import pandas as pd


sh_path = "/mnt/hgfs/share_with_ub/SH"
class Command(BaseCommand):

    def handle(self, *args, **options):
        sh_files = os.listdir(sh_path)
        for sh_file in sh_files:
            tick_data = pd.read_csv(f"{sh_path}/{sh_file}", encoding="gbk", header=1)[:-1]
            print("xxx")