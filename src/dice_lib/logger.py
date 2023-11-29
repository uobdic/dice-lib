from fasthep_logging import get_logger
import logging

APP_LOGGER_NAME = "DICE::LIB"

log = get_logger(APP_LOGGER_NAME)
log.debug("Logging initialised")
log.setLevel(logging.INFO)
