"""
    Tests the open_webdriver package.
"""

import unittest

from open_webdriver.open_webdriver import open_webdriver


def do_google_test(headless: bool) -> bool:
    """Runs the tests for a given driver."""
    with open_webdriver(headless=headless, verbose=True) as driver:
        driver.get("https://www.google.com")
        return driver.title == "Google"


class OpenWebDriverTests(unittest.TestCase):
    """Tester for open_webdriver.py"""

    def test_google(self) -> None:
        """Tests that google test works."""
        ok = do_google_test(headless=False)  # pylint: disable=invalid-name
        self.assertTrue(ok)

    def test_google_headless(self) -> None:
        """Tests that google headless works."""
        ok = do_google_test(headless=True)  # pylint: disable=invalid-name
        self.assertTrue(ok)


def package_tests() -> None:
    """Package tests to be run on the command line to ensure open_webdriver works on the system."""

    try:
        _ = do_google_test(headless=True)
        print("\nopen_webdriver_test completed successfully.\n")
        return
    except Exception as err:  # pylint: disable=broad-except
        from open_webdriver.path import (  # pylint: disable=import-outside-toplevel
            LOG_FILE,
        )

        try:
            with open(LOG_FILE, encoding="utf-8", mode="r") as filed:
                print(filed.read())
        except Exception as err2:  # pylint: disable=broad-except
            print(f"Error reading log file {LOG_FILE} because {err2}")

        print(f"{__file__}: Error: {err}")
        print("\n  FAILED: open_webdriver_test")
        return


def main():
    """Runs the tests."""
    unittest.main()


if __name__ == "__main__":
    main()
