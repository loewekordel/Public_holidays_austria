import os
import sqlite3
import datetime
from dataclasses import dataclass
import logging
import contextlib
from typing import Any
from typing import Generator
from typing import Optional

logger = logging.getLogger("public_holidays")


@dataclass
class PublicHoliday:
    name: str
    date: datetime.date
    weekday: int

    def __post_init__(self):
        pass


class Model:
    def __init__(self, path: str = ":memory:") -> None:
        self.path = path

        if self.path == ":memory:" or os.path.exists(self.path):
            return

        with self._connect() as db:
            db.executescript(
                "CREATE TABLE public_holidays ("
                "    year INTEGER NOT NULL,"
                "    month INTEGER NOT NULL,"
                "    day INTEGER NOT NULL,"
                "    weekday INTEGER NOT NULL,"
                "    name TEXT NOT NULL,"
                "    PRIMARY KEY (year, month, day)"
                ");",
            )

    @contextlib.contextmanager
    def _connect(
        self,
        path: Optional[str] = None,
    ) -> Generator[sqlite3.Connection, None, None]:
        path = path or self.path
        # See: https://stackoverflow.com/a/28032829/812183
        with contextlib.closing(sqlite3.connect(path)) as conn:
            # this creates a transaction
            with conn:  # auto-commits
                yield conn

    def add(self, _date: datetime.date, name: str) -> None:
        with self._connect() as db:
            db.execute(
                """INSERT INTO public_holidays VALUES(?, ?, ?, ?, ?)""",
                (_date.year, _date.month, _date.day, _date.isoweekday(), name),
            )

    def get(self, _year: int, _name: str) -> PublicHoliday:
        with self._connect() as db:
            row = db.execute(
                "SELECT * FROM public_holidays WHERE year = ? and name = ?",
                (
                    _year,
                    _name,
                ),
            ).fetchone()
            year, month, day, weekday, name = row
            return PublicHoliday(name, datetime.date(year, month, day), weekday)

    def get_all(self) -> list[str]:
        with self._connect() as db:
            rows = db.execute("SELECT * FROM public_holidays").fetchall()
            return [
                PublicHoliday(name, datetime.date(year, month, day), weekday)
                for year, month, day, weekday, name in rows
            ]

    def get_yearly(self, year: int, weekday_only=False) -> list[PublicHoliday]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT * FROM public_holidays WHERE year = ? and weekday BETWEEN 1 and ?",
                (year, 5 if weekday_only else 7),
            ).fetchall()
            return [
                PublicHoliday(name, datetime.date(year, month, day), weekday)
                for year, month, day, weekday, name in rows
            ]

    def query(self, q: str) -> Any:
        with self._connect() as db:
            return db.execute(q).fetchall()
