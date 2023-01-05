import datetime
import argparse
import logging
from typing import Callable
from typing import Sequence
from typing import Optional
import yaml
from public_holidays.model import Model
from public_holidays.view import View
from public_holidays import dynamic_days

logger = logging.getLogger("public_holidays")


def load_config(path: str) -> dict[str, str | int]:
    with open(path) as f:
        return yaml.safe_load(f)


class Cli:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def _feed_db(self, year: int, config: dict[str, str | int]):
        for name, values in config.items():
            if "month" in values and "day" in values:
                self.model.add(
                    datetime.date(year=year, month=values["month"], day=values["day"]),
                    name,
                )
            elif "func" in values:
                calc_date_func: Callable[[int], datetime.date] = getattr(
                    dynamic_days, values["func"]
                )
                date = calc_date_func(year)
                self.model.add(
                    datetime.date(year=date.year, month=date.month, day=date.day), name
                )
            elif "base_name" in values and "offset" in values:
                base_holiday = self.model.get(year, values["base_name"])
                new_holiday = base_holiday.date + datetime.timedelta(
                    days=values["offset"]
                )
                self.model.add(
                    datetime.date(
                        year=new_holiday.year,
                        month=new_holiday.month,
                        day=new_holiday.day,
                    ),
                    name,
                )
            else:
                raise KeyError(f"unknown set of keys in '{name}'")

    def run(self, argv: Optional[Sequence[str]] = None) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "year", type=int, help="year or start year if used with 'number' argument"
        )
        parser.add_argument(
            "-n", "--number", type=int, default=0, help="number of consecutive years"
        )
        parser.add_argument("-q", "--query")
        parser.add_argument(
            "-c", "--config", default="austria.yml", help="public holiday yaml config"
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="increase output verbosity",
        )
        args = parser.parse_args(argv)

        # add logging to console
        sh = logging.StreamHandler()
        sh.setFormatter(logger.parent.handlers[0].formatter)
        logger.addHandler(sh)
        if args.verbose > 0:
            logger.setLevel(logging.DEBUG)

        # load public holidays config
        config = load_config(args.config)

        # feed the database with the public holidays data of the specified years
        for year in range(args.year, args.year + args.number + 1, 1):
            self._feed_db(year, config)

            logging.debug(self.model.get_all())

            # view requested data
            # self.view.all_weekday(args.year)
            self.view.num_all_weekday(year)

            if args.query:
                p = self.model.query(args.query)
                logging.info(p)
