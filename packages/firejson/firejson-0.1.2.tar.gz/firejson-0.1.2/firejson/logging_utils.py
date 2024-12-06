import logging

# Logging utils
def set_logger():
    """
    Sets up the logger with console and file handlers.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("firejson")

    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger

    # Set log level
    logger.setLevel(logging.DEBUG)

    # Console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # File logging
    file_handler = logging.FileHandler("firejson.log", mode='w')  # Overwrite each time
    file_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_success(logger, message):
    """
    Logs a success message.

    Args:
        logger (logging.Logger): Logger instance.
        message (str): Success message.
    """
    logger.info(message)


def log_error(logger, message, error=None):
    """
    Logs an error message with optional exception details.

    Args:
        logger (logging.Logger): Logger instance.
        message (str): Error message.
        error (Exception, optional): Exception to include in the log. Defaults to None.
    """
    if error:
        logger.error(f"{message}: {error}")
    else:
        logger.error(message)