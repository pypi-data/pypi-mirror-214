import logging

from colorlog import ColoredFormatter

logger = logging.getLogger("kaxi")


def init(verbose, **kwargs):
    if verbose:
        if verbose == "debug":
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

    # define handler and formatter
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s   %(asctime)s%(reset)s | %(log_color)s%(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # add formatter to handler
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)
