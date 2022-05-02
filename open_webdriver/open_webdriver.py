"""
    Handles the creation of the web driver.
"""

import os
import sys
from typing import Any

from selenium.webdriver import ChromeOptions  # type: ignore
from selenium.webdriver import FirefoxOptions
from webdriver_setup import get_webdriver_for  # type: ignore
from webdriver_setup.driver import DriverBase as Driver  # type: ignore

# Turn off SSL verification to allow visiting websites with self-signed certs.
os.environ["WDM_SSL_VERIFY"] = "0"
os.environ["WDM_LOCAL"] = "1"

FORCE_HEADLESS = sys.platform == "linux" and "DISPLAY" not in os.environ
DEFAULT_DRIVER = "chrome"


def open_webdriver(driver_name: str = DEFAULT_DRIVER, headless: bool = True) -> Driver:
    """Opens the web driver."""

    opts: Any = None
    if headless or FORCE_HEADLESS:
        if FORCE_HEADLESS and not headless:
            print("\n  WARNING: HEADLESS ENVIRONMENT DETECTED, FORCING HEADLESS")
        if driver_name in ["chrome", "brave"]:
            opts = ChromeOptions()
            opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--disable-dev-shm-usage")
        elif driver_name == "firefox":
            opts = FirefoxOptions()
            opts.headless = True
        else:
            raise NotImplementedError(
                f"{__file__}: headless mode for {driver_name} is not supported."
            )
    if driver_name == "firefox":
        print(f"{__file__}: Warning: firefox browser has known issues.")
    driver = get_webdriver_for(browser=driver_name, options=opts)
    return driver
