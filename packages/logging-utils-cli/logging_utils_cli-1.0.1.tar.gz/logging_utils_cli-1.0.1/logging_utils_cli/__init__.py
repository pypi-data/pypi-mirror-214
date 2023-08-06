import logging
import sys

from .utils import add_logging_level

add_logging_level("SUCCESS", logging.INFO + 5)
from .formatter import TerminalFormatter  # noqa: E402


def get_terminal_log_handler() -> logging.StreamHandler:
    terminal_log_handler = logging.StreamHandler(stream=sys.stderr)
    terminal_log_handler.setFormatter(TerminalFormatter())
    return terminal_log_handler
