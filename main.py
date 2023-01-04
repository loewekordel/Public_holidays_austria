#! usr/bin/python3

import sys
import argparse
import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Sequence

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


class Weekday(Enum):
    Montag: auto()
    Dienstag: auto()
    Mittwoch: auto()
    Donnerstag: auto()
    Freitag: auto()
    Samstag: auto()
    Sonntag: auto()


@dataclass
class PublicHoliday:
    name: str
    date: tuple[int, int]
    weekday: Weekday

    def __post_init__(self):
        self.month, self.day = self.date


public_holidays = [
    PublicHoliday("Neujahr", (1, 1), None),
    PublicHoliday("Heilige Drei Könige", (1, 6), None),
    PublicHoliday("Ostersonntag", (0, 0), "Sunday"),
    PublicHoliday("Ostermontag", (0, 0), "Monday"),
    PublicHoliday("Staatsfeiertag", (5, 1), None),
    # 39 days after Ostersonntag, therefore always a "Donnerstag"
    PublicHoliday("Christi Himmelfahrt", (0, 0), "Thursday"),
    PublicHoliday("Pfingstsonntag", (0, 0), "Sunday"),
    PublicHoliday("Pfingstmontag", (0, 0), "Monday"),
    # 60 days after Ostersonntag, therefore always a "Donnerstag"
    PublicHoliday("Fronleichnam", (0, 0), "Thursday"),
    PublicHoliday("Mariä Himmelfahrt", (8, 15), None),
    PublicHoliday("Nationalfeiertag", (10, 26), None),
    PublicHoliday("Allerheiligen", (11, 1), None),
    PublicHoliday("Mariä Empfängnis", (12, 8), None),
    PublicHoliday("Christtag", (12, 25), None),
    PublicHoliday("Stefanitag", (12, 26), None),
]


def main(argv: Optional[Sequence[int]] = None):

    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("-n", "--number", type=int, default=0)
    args = parser.parse_args(argv)

    for year in range(args.year, args.year + args.number + 1, 1):
        free_days = 0
        for public_holiday in public_holidays:
            if public_holiday.weekday is None:
                weekday = weekdays[datetime.date(year, *public_holiday.date).weekday()]
            else:
                weekday = public_holiday.weekday

            if weekday not in ["Saturday", "Sunday"]:
                free_days += 1

            # print(f"{year}/{public_holiday.month:>2}/{public_holiday.day:>2} = {weekday}")

        print(f"free days {year}: {free_days}")


if __name__ == "__main__":
    sys.exit(main())
