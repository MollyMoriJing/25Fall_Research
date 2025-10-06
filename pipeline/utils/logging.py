import logging


def get_logger():
    # basic stdout logger
    logger = logging.getLogger("pipeline_v1")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        h = logging.StreamHandler()
        f = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        h.setFormatter(f)
        logger.addHandler(h)
    return logger


