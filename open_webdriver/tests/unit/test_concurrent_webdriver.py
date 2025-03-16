"""
Tests the open_webdriver package.
"""

import threading
import unittest

from open_webdriver.main import open_webdriver


def do_google_test() -> bool:
    """Runs the tests for a given driver."""
    with open_webdriver(verbose=True) as driver:
        driver.get("https://www.google.com")
        return driver.title == "Google"


class ConcurrentTests(unittest.TestCase):
    """Tester for open_webdriver.py"""

    def test_concurrent(self) -> None:
        """Tests that google test works."""

        # Create a thread that runs the function.
        th1 = threading.Thread(target=do_google_test)
        th2 = threading.Thread(target=do_google_test)
        th1.start()
        th2.start()
        th1.join(timeout=60 * 10)
        th2.join(timeout=60 * 10)
        if th1.is_alive():
            print("Thread 1 timed out.")
        if th2.is_alive():
            print("Thread 2 timed out.")


def main():
    """Runs the tests."""
    unittest.main()


if __name__ == "__main__":
    main()
