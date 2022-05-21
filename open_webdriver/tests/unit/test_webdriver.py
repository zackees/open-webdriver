"""
    Tests the open_webdriver package.
"""

import os
import sys
import unittest

from open_webdriver.open_webdriver import open_webdriver

FULL_TESTS = os.environ.get("FULL_TESTS", "0") == "0"

if FULL_TESTS:
    all_drivers = ["chrome", "firefox"]
else:
    all_drivers = ["chrome"]


def do_google_test(driver_name: str, headless: bool) -> bool:
    """Runs the tests for a given driver."""
    with open_webdriver(driver_name=driver_name, headless=headless, verbose=True) as driver:
        driver.get("https://www.google.com")
        return driver.title == "Google"


class OpenWebDriverTests(unittest.TestCase):
    """Tester for open_webdriver.py"""

    @unittest.skipIf(sys.platform != "win32", "Windows only tests")
    def test_win32_bug(self) -> None:
        """Asserts that the win32 bug is fixed."""
        with open_webdriver():
            pass
        # This environmental variable should be available now.
        self.assertIn("PROGRAMW6432", os.environ)

    def test_google(self) -> None:
        """Tests that google test works."""
        for driver in all_drivers:
            ok = do_google_test(driver, headless=False)  # pylint: disable=invalid-name
            self.assertTrue(ok)

    def test_google_headless(self) -> None:
        """Tests that google headless works."""
        for driver in all_drivers:
            ok = do_google_test(driver, headless=True)  # pylint: disable=invalid-name
            self.assertTrue(ok)


def package_tests() -> None:
    """Package tests to be run on the command line to ensure open_webdriver works on the system."""
    try:
        _ = do_google_test("chrome", headless=True)
        print("\nopen_webdriver_test completed successfully.\n")
        return
    except Exception as err:  # pytype: disable=broad-except
        print(f"{__file__}: Error: {err}")
        print("\n  FAILED: open_webdriver_test")
        return


def main():
    """Runs the tests."""
    unittest.main()


if __name__ == "__main__":
    main()
