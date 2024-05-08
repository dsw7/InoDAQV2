from logging.config import dictConfig


def setup_logger() -> None:
    logging_config = {
        "version": 1,
        "formatters": {
            "debug": {
                "format": "%(name)s %(asctime)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            }
        },
        "handlers": {
            "stream": {
                "formatter": "debug",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "werkzeug": {
                "level": "DEBUG",
                "handlers": ["stream"],
            },
            "inodaqv2": {
                "level": "DEBUG",
                "handlers": ["stream"],
            },
        },
    }

    dictConfig(logging_config)
