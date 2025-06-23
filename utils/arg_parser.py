import argparse
import logging

class Args:

    @staticmethod
    def _get_parser():
        parser = argparse.ArgumentParser(
            description="Automation Framework CLI",
        )

        # Parent-level arguments
        parser.add_argument(
            "--config", type=str, default="config/pi3_config.json",
            help="Path to device configuration YAML file"
        )
        parser.add_argument(
            "--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO", help="Logging level"
        )

        parser.add_argument(
            "--system_testing", type=str, required=True, help="system for testing"
        )

        return parser

    @staticmethod
    def parse_args():
        parser = Args._get_parser()
        args = parser.parse_args()

        return args