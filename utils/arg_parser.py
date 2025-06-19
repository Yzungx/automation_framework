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
            "--config", type=str, default="config/device_config.yaml",
            help="Path to device configuration YAML file"
        )
        parser.add_argument(
            "--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO", help="Logging level"
        )

        return parser

    @staticmethod
    def parse_args():
        parser = Args._get_parser()
        args = parser.parse_args()

        return args