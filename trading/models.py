from common import models
from .constants import InstStatus


class Instruments(models.Model):
    iuid = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=8)
    board = models.CharField(max_length=3)
    base_volatility = models.DecimalField(max_digits=6, decimal_places=3)
    base_volume = models.DecimalField(max_digits=20, decimal_places=10)
    avg_volatility_12M = models.DecimalField(max_digits=6, decimal_places=3)  # 波动以千分之一
    avg_volatility_3M = models.DecimalField(max_digits=6, decimal_places=3)
    avg_volatility_1M = models.DecimalField(max_digits=6, decimal_places=3)
    avg_volatility_1W = models.DecimalField(max_digits=6, decimal_places=3)
    avg_volume_12M = models.DecimalField(max_digits=20, decimal_places=10)  # 成交量以万为单位
    avg_volume_6M = models.DecimalField(max_digits=20, decimal_places=10)
    avg_volume_3M = models.DecimalField(max_digits=20, decimal_places=10)
    avg_volume_1M = models.DecimalField(max_digits=20, decimal_places=10)
    avg_volume_1W = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.PositiveTinyIntegerField(default=InstStatus.ACTIVE,
                                             choices=InstStatus.VALUE_TO_NAME.items())

    class Meta:
        db_table = 'instruments'