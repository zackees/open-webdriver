"""
    Tests the open_webdriver package.
"""

import unittest

from open_webdriver import open_webdriver

FULL_TESTS = False

if FULL_TESTS:
    all_drivers = ["chrome", "firefox", "brave"]
else:
    all_drivers = ["chrome"]


def do_test(driver_name: str, headless: bool) -> bool:
    """Runs the tests for a given driver."""
    with open_webdriver(driver_name=driver_name, headless=headless, verbose=True) as driver:
        driver.get("https://www.google.com")
        return driver.title == "Google"


class GabDriverTest(unittest.TestCase):
    """Gab driver test framework."""

    def test_gab_test(self) -> None:
        """Tests that gab_test works."""
        for driver in all_drivers:
            ok = do_test(driver, headless=False)  # pylint: disable=invalid-name
            self.assertTrue(ok)

    def test_gab_test_headless(self) -> None:
        """Tests that gab_test works."""
        for driver in all_drivers:
            ok = do_test(driver, headless=True)  # pylint: disable=invalid-name
            self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
