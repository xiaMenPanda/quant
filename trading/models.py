from common import models
from .constants import InstStatus


class Instruments(models.Model):
    iuid = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=8)
    board = models.CharField(max_length=3)
    base_volatility = models.FloatField()
    base_volume = models.FloatField()
    avg_volume_three_days_div_two_weeks = models.FloatField()
    avg_volume_one_week_div_one_month = models.FloatField()
    avg_volume_two_weeks_div_two_months = models.FloatField()
    avg_volume_one_month_div_one_year = models.FloatField()
    avg_abs_volatility_three_days_div_two_weeks = models.FloatField()
    avg_abs_volatility_one_week_div_one_month = models.FloatField()
    avg_abs_volatility_two_weeks_div_two_months = models.FloatField()
    avg_abs_volatility_one_month_div_one_year = models.FloatField()
    cal_size_on_day = models.FloatField()
    cal_size_two_days = models.FloatField()
    cal_size_three_days = models.FloatField()
    cal_size_one_week = models.FloatField()
    cal_size_two_weeks = models.FloatField()
    cal_size_one_month = models.FloatField()
    cal_size_two_months = models.FloatField()
    cal_size_three_months = models.FloatField()
    cal_size_six_months = models.FloatField()
    cum_volatility_one_week = models.FloatField()
    cum_volatility_two_weeks = models.FloatField()
    cum_volatility_one_month = models.FloatField()
    cum_volatility_two_months = models.FloatField()
    cum_volatility_three_months = models.FloatField()
    cum_volatility_six_months = models.FloatField()
    status = models.PositiveTinyIntegerField(default=InstStatus.ACTIVE,
                                             choices=InstStatus.VALUE_TO_NAME.items())

    class Meta:
        db_table = 'instruments'