"""
    Module for the Open Webdriver.
"""

import os

from .open_webdriver import Driver  # type: ignore
from .open_webdriver import open_webdriver
from .path import LOG_FILE

if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)


def test() -> None:
    """Runs the tests."""
    from .tests.unit import test_webdriver  # pylint: disable=import-outside-toplevel

    test_webdriver.package_tests()
