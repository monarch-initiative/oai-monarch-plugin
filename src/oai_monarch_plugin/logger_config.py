from loguru import logger
import sys

def configure_logger():
    logger.remove()  # remove the default handler

    # info goes to stdout, warning and above go to stderr
    def info_filter(record):
        return record["level"].name == "INFO"

    def warning_filter(record):
        return record["level"].name in ["WARNING", "ERROR", "CRITICAL"]

    logger.add(sys.stdout, format="{time} {level} {message}", filter=info_filter)
    logger.add(sys.stderr, format="{time} {level} {message}", filter=warning_filter)

    logger.propagate = False  # don't propagate to the root logger
