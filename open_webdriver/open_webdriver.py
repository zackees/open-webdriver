"""
    Handles the creation of the web driver.
"""

# pylint: disable=protected-access

import logging
import os
import ssl
import sys
from typing import Any

import urllib3  # type: ignore
from selenium.webdriver import ChromeOptions  # type: ignore
from selenium.webdriver import FirefoxOptions
from webdriver_setup import get_webdriver_for  # type: ignore
from webdriver_setup.driver import DriverBase as Driver  # type: ignore

urllib3.disable_warnings()

ssl._create_default_https_context = ssl._create_unverified_context

# Turn off SSL verification to allow visiting websites with self-signed certs.
os.environ["WDM_SSL_VERIFY"] = "0"
if "WDM_LOCAL" not in os.environ:
    os.environ["WDM_LOCAL"] = "1"

FORCE_HEADLESS = sys.platform == "linux" and "DISPLAY" not in os.environ
DEFAULT_DRIVER = "chrome"


def open_webdriver(
    driver_name: str = DEFAULT_DRIVER, headless: bool = True, verbose: bool = False
) -> Driver:
    """Opens the web driver."""

    opts: Any = None

    if headless or FORCE_HEADLESS:
        if FORCE_HEADLESS and not headless:
            print("\n  WARNING: HEADLESS ENVIRONMENT DETECTED, FORCING HEADLESS")
        headless = True

    if driver_name in ["chrome", "brave"]:
        # For Chrome/Brave just install the driver immediately.
        opts = ChromeOptions()
        opts.add_argument("--ignore-certificate-errors")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        if headless:
            opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")
    elif driver_name == "firefox":
        print(f"{__file__}: Warning: firefox browser has known issues.")
        opts = FirefoxOptions()
        opts.accept_insecure_certs = True
        if headless:
            opts.headless = True
    else:
        raise NotImplementedError(
            f"Unsupported driver name: {driver_name}. Supported drivers: chrome, firefox, brave."
        )
    # Don't spam the console with warnings.
    try:
        if not verbose:
            logging.captureWarnings(True)
        driver = get_webdriver_for(browser=driver_name, options=opts)
    finally:
        if not verbose:
            logging.captureWarnings(False)
    return driver
