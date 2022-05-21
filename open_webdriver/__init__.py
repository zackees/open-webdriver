"""
    Module for the Open Webdriver.
"""

from .open_webdriver import Driver  # type: ignore
from .open_webdriver import open_webdriver


def test() -> None:
    """Runs the tests."""
    from .tests.unit import test_webdriver  # pylint: disable=import-outside-toplevel

    test_webdriver.package_tests()
