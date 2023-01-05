import datetime
from public_holidays.dynamic_days import gauss_easter_adapted

def test_gauss_easter_adapted():
    assert gauss_easter_adapted(2022) == datetime.date(2022, 4, 17)
