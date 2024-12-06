import logging


def setup_logger(name: str = "", level: int = logging.DEBUG) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    name = name or "bbsky"
    logger_ = logging.getLogger(name)
    logger_.setLevel(level)
    return logger_


logger = setup_logger()
