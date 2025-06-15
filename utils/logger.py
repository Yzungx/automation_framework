import argparse
import logging
from typing import Optional

class LoggerSetup:
    """
    A class to set up and manage logging configuration based on command-line arguments.

    Attributes:
        log_level (str): The current log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
        logger (logging.Logger): The configured logger instance.
    """

    def __init__(self, default_log_level: str = "INFO"):
        """
        Initialize the LoggerSetup with a default log level.

        Args:
            default_log_level (str): The default log level if not specified (default: INFO).
        """
        self.log_level = default_log_level.upper()
        self.logger = None
        self._setup_parser()

    def _setup_parser(self) -> None:
        """Set up the argument parser for command-line arguments."""
        self.parser = argparse.ArgumentParser(description="A script with configurable log level.")
        self.parser.add_argument(
            '--log-level',
            type=str,
            default=self.log_level,
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            help="Set the logging level (default: INFO)"
        )

    def configure_logging(self) -> None:
        """
        Configure the logging system based on the provided or parsed log level.

        Returns:
            None
        """
        # Parse arguments
        args = self.parser.parse_args()

        # Update log level from arguments
        self.log_level = args.log_level.upper()

        # Map log level to numeric value
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        numeric_level = level_map.get(self.log_level, logging.INFO)

        # Create or get logger
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            logging.basicConfig(
                level=numeric_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            self.logger.setLevel(numeric_level)

        # Log the setup completion
        self.logger.debug("Logging setup completed with level: %s", self.log_level)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger.
        """
        if self.logger is None:
            self.configure_logging()
        return self.logger

    def log_example_messages(self) -> None:
        """
        Log example messages at different levels for demonstration.
        """
        logger = self.get_logger()
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