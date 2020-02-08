from common import models
from .constants import InstStatus


class Instruments(models.Model):
    iuid = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=8)
    board = models.CharField(max_length=3)
    base_volatility = models.FloatField()
    base_volume = models.FloatField()
    status = models.PositiveTinyIntegerField(default=InstStatus.ACTIVE,
                                             choices=InstStatus.VALUE_TO_NAME.items())
    size_in_file = models.IntegerField()


    class Meta:
        db_table = 'instruments'