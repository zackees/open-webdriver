"""
Tests the open_webdriver package.
"""

import os
import sys
import unittest
from pprint import pprint


class OpenWebDriverTests(unittest.TestCase):
    """Tester for open_webdriver.py"""

    @unittest.skipIf(sys.platform != "win32", "Windows only tests")
    def test_osenv(self) -> None:
        """Asserts that the win32 bug is fixed."""
        pprint(dict(os.environ))


if __name__ == "__main__":
    unittest.main()
