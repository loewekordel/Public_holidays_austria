from datetime import date


def gauss_easter_adapted(year: int) -> date:
    """
    Calculate easter date
    Reference: https://de.wikipedia.org/wiki/Gau%C3%9Fsche_Osterformel#Eine_erg%C3%A4nzte_Osterformel
    :param year: year to get easter date for
    :return: datetime easter date
    """
    k = year // 100
    m = 15 + (3 * k + 3) // 4 - (8 * k + 13) // 25
    s = 2 - (3 * k + 3) // 4
    a = year % 19
    d = (19 * a + m) % 30
    r = (d + a // 11) // 29
    og = 21 + d - r
    sz = 7 - (year + year // 4 + s) % 7
    oe = 7 - (og - sz) % 7
    os = og + oe

    return date(year, 4 if os > 31 else 3, os - 31 if os > 31 else os)
