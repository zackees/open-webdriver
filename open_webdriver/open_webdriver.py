"""
    Handles the creation of the web driver.
"""

# pylint: disable=protected-access

import os
import ssl
import sys
import time
import traceback
from typing import Any

import urllib3  # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver import ChromeOptions  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from webdriver_manager.driver import Driver  # type: ignore

from open_webdriver.download_chromium import get_chromium_exe
from open_webdriver.path import LOG_FILE, WDM_DIR

urllib3.disable_warnings()

ssl._create_default_https_context = ssl._create_unverified_context

# Turn off SSL verification to allow visiting websites with self-signed certs.
os.environ["WDM_SSL_VERIFY"] = "0"

FORCE_HEADLESS = sys.platform == "linux" and "DISPLAY" not in os.environ

CACHE_TIMEOUT = 7


def open_webdriver(
    headless: bool = True,
    verbose: bool = False,  # pylint: disable=unused-argument
) -> Driver:
    """Opens the web driver."""

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, encoding="utf-8", mode="w") as filed:
        filed.write(f"{__file__}: Starting up web driver.\n")
        if sys.platform == "linux":
            if os.geteuid() == 0:
                filed("\n\n  WARNING: Running as root. The driver may crash!\n\n")
    opts: Any = None
    if headless or FORCE_HEADLESS:
        if FORCE_HEADLESS and not headless:
            print("\n  WARNING: HEADLESS ENVIRONMENT DETECTED, FORCING HEADLESS")
        headless = True
    # For Chrome/Brave just install the driver immediately.
    opts = ChromeOptions()
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    if headless:
        opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
    if sys.platform != "darwin":
        chromium_exe = get_chromium_exe()
        opts.binary_location = chromium_exe
    driver_path = ChromeDriverManager(cache_valid_range=CACHE_TIMEOUT, path=WDM_DIR).install()
    if verbose:
        print(f"\n  Using ChromeDriver: {driver_path}")
    try:
        driver = webdriver.Chrome(driver_path, options=opts, service_log_path=LOG_FILE)
        return driver
    except Exception as err:  # pylint: disable=broad-except
        traceback.print_exc()
        print(f"{__file__}: Error: {err}")
        print(f"Please see:\n  {LOG_FILE}")
        raise


if __name__ == "__main__":
    open_webdriver()
