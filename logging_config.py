import logging
from datetime import datetime

LOGGING_FILENAME = "logs.txt"
DATA_FILENAME = f"log2023-08-24.log.csv"


def configure_logging():
    logging.basicConfig(
        filename=LOGGING_FILENAME,
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s(%(levelname)s)[%(threadName)s]: %(message)s",
        datefmt="%d.%m.%Y %I:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s(%(levelname)s)[%(threadName)s]: %(message)s", "%d.%m.%Y %I:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    # configure data logger
    data_logger = logging.getLogger("data")
    file_handler = logging.FileHandler(DATA_FILENAME, encoding="utf8")
    file_handler.setLevel(logging.DEBUG)
    data_logger.addHandler(file_handler)
    data_logger.propagate = False
