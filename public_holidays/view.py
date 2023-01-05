import os
import logging
from public_holidays.model import Model

logger = logging.getLogger("public_holidays")


class View:
    def __init__(self, model: Model) -> None:
        self.model = model

    def all_weekday(self, year: int) -> None:
        logger.info(
            "Public holidays on weekdays:\n"
            f"{os.linesep.join([str(d) for d in self.model.get_yearly(year, weekday_only=True)])}"
        )

    def num_all_weekday(self, year: int) -> None:
        logger.info(
            f"public_holidays on weekdays in {year}: "
            f"{len(self.model.get_yearly(year, weekday_only=True)):>2}"
        )
