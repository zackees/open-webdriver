"""
    Module for the Open Webdriver.
"""

import os

from .main import Driver  # type: ignore
from .main import open_webdriver
from .path import LOG_FILE


def test() -> None:
    """Runs the tests."""
    from .tests.unit import test_webdriver  # pylint: disable=import-outside-toplevel

    test_webdriver.package_tests()
