import os
import logging
from typing import Sequence, Optional
from public_holidays import Cli, Model, View


def main(argv: Optional[Sequence[str]] = None) -> int:
    db_name = "db.db"
    logging.basicConfig(
        filename="main.log",
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    logging.info("main")

    if os.path.exists(db_name):
        os.remove(db_name)
    model = Model(db_name)
    view = View(model)
    cli = Cli(model, view)
    cli.run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
