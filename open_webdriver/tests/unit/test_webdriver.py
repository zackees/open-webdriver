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
    except Exception as err:  # pylint: disable=broad-except
        print(f"\nFAILED: open_webdriver_test because of {err}")


def main():
    """Runs the tests."""
    unittest.main()


if __name__ == "__main__":
    main()
