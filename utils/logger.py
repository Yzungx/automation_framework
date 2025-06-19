import argparse
import logging
from typing import Optional

class LoggerSetup:

    @staticmethod
    def get_logger(name: Optional[str] = None, log_level: str = "INFO") -> logging.Logger:
        """
        Quickly configure and return a logger with the specified log level.

        Args:
            name (str): Logger name (__name__).
            log_level (str): Logging level as string (DEBUG, INFO, etc.).

        Returns:
            logging.Logger: Configured logger instance.
        """
        log_level = log_level.upper()

        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        numeric_level = level_map.get(log_level, logging.INFO)

        logger = logging.getLogger(name)

        if not logger.handlers:
            # Only configure once
            logging.basicConfig(
                level=numeric_level,
                format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            logger.setLevel(numeric_level)

        return logger

    def log_example_messages(self, log_level: str = 'INFO') -> None:
        """
        Log example messages at different levels for demonstration.
        """
        logger = self.get_logger(name=__name__, log_level=log_level)
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")

# def main():
#     # Create an instance of LoggerSetup
#     logger_setup = LoggerSetup()

#     # Configure logging
#     logger_setup.configure_logging()

#     # Log example messages
#     logger_setup.log_example_messages()

# if __name__ == "__main__":
#     main()

# python logger.py --log-level ERROR