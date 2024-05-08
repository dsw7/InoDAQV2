from logging.config import dictConfig

dictConfig(
    {
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
            "inodaqv2": {
                "level": "DEBUG",
                "handlers": ["stream"],
            },
        },
    }
)
