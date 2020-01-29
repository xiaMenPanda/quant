from common.enum_type import EnumBase

class InstStatus(EnumBase):
    UNACTIVE = 0
    DATA_PROBLEM = 1
    SPECIAL = 2
    ACTIVE = 3


DATE_TIME_FORMATE = '%Y-%m-%d'

SECOND = 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7