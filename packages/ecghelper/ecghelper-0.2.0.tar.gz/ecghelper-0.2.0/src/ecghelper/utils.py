import logging


def create_logger(name: str, level=logging.INFO):
    """Create a logger local to the file."""
    _LOGGER = logging.getLogger(name)
    _HANDLER = logging.StreamHandler()
    _FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    _HANDLER.setFormatter(_FORMATTER)
    _LOGGER.addHandler(_HANDLER)
    _LOGGER.setLevel(level)
    return _LOGGER
