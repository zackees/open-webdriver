"""
Tests the open_webdriver package.
"""

import os
import sys
import unittest


class CommandTest(unittest.TestCase):
    """Tests that the command open_webdriver_test executes."""

    @unittest.skipIf(sys.platform != "win32", "Windows only tests")
    def test_cmd(self) -> None:
        """Asserts that the win32 bug is fixed."""
        self.assertEqual(0, os.system("open_webdriver_test"))


def main():
    """Runs the tests."""
    unittest.main()


if __name__ == "__main__":
    main()
