from common.enum_type import EnumBase

class InstStatus(EnumBase):
    UNACTIVE = 0
    DATA_PROBLEM = 1
    SPECIAL = 2
    ACTIVE = 3
    RESEARCH = 4


DATE_TIME_FORMATE = '%Y-%m-%d'

SECOND = 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7
MONTH = DAY * 31
YEAR = MONTH * 12


RESEARCH_BOARTS = ["SH", "MSB", "GEM", "SZ"]

INDEX_MAP = {
    "SH": "999999",
    "SZ": "399001",
    "MSB": "399005",
    "GEM": "399006"
}


# class DURATION(EnumBase):
#     SO_FAR = YEAR * 5
#     ONE_YEAR = YEAR
#     SIX_MONTHS = MONTH * 6
#     THREE_MONTHS = MONTH * 3
#     ONE_MONTH = MONTH
#     THREE_WEEKS = WEEK * 3
#     TWO_WEEKS = WEEK * 2
#     ONE_WEEK = WEEK


class DURATION(EnumBase):
    ONE_DAY = 1
    TWO_DAYS = 2
    THREE_DAYS = 3
    ONE_WEEK = 5
    TWO_WEEKS = 10
    THREE_WEEKS = 15
    ONE_MONTH = 20
    TWO_MONTHS = 40
    THREE_MONTHS = 60
    SIX_MONTHS = 130
    ONE_YEAR = 260


RESEARCH_FACTORS = ["avg_abs_volatility", "avg_volume", "cumulative_volatility"]