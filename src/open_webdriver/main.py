"""
Handles the creation of the web driver.
"""

# pylint: disable=protected-access

import os
import ssl
import sys
import traceback
from typing import Optional

import filelock  # type: ignore
import urllib3  # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver import ChromeOptions  # type: ignore
from selenium.webdriver.remote.webdriver import WebDriver as Driver  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from webdriver_manager.core.driver_cache import DriverCacheManager  # type: ignore

from open_webdriver.download_chromium import get_chromium_exe
from open_webdriver.path import LOG_FILE, WDM_DIR

urllib3.disable_warnings()

ssl._create_default_https_context = ssl._create_unverified_context

# Turn off SSL verification to allow visiting websites with self-signed certs.
os.environ["WDM_SSL_VERIFY"] = "0"

FORCE_HEADLESS = sys.platform == "linux" and "DISPLAY" not in os.environ

CACHE_TIMEOUT_DAYS = 7

os.makedirs(WDM_DIR, exist_ok=True)
LOCK_FILE = os.path.join(WDM_DIR, "lock.file")

INSTALL_TIMEOUT = float(60 * 10)  # Upto 10 minutes of install time.

# CHROME_VERSION = "136.0.7071.0"
CHROME_VERSION = None


def _user_agent(chrome_version: str | None = None) -> str:
    """Gets the user agent."""
    chrome_version = chrome_version or "136.0.7071.0"
    return (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        f" Chrome/{chrome_version} Safari/537.36"
    )


def open_webdriver(  # pylint: disable=too-many-arguments,too-many-branches
    headless: bool = True,
    verbose: bool = False,  # pylint: disable=unused-argument
    timeout: float = INSTALL_TIMEOUT,
    disable_gpu: Optional[bool] = None,
    disable_dev_shm_usage: bool = True,
    user_agent: str | None = None,
) -> Driver:
    """Opens the web driver."""
    user_agent = user_agent or _user_agent()
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, encoding="utf-8", mode="w") as filed:
        filed.write(f"{__file__}: Starting up web driver.\n")
        if sys.platform == "linux":
            if os.geteuid() == 0:
                filed.write("\n\n  WARNING: Running as root. The driver may crash!\n\n")
    if headless or FORCE_HEADLESS:
        if FORCE_HEADLESS and not headless:
            print("\n  WARNING: HEADLESS ENVIRONMENT DETECTED, FORCING HEADLESS")
        headless = True
    # For Chrome/Brave just install the driver immediately.
    opts: ChromeOptions = ChromeOptions()
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--no-sandbox")
    if disable_dev_shm_usage:
        opts.add_argument("--disable-dev-shm-usage")
    if headless:
        opts.add_argument("--headless")
        if disable_gpu is None or disable_gpu is True:
            opts.add_argument("--disable-gpu")
    if user_agent:
        opts.add_argument(f"--user-agent={user_agent}")
    lock = filelock.FileLock(LOCK_FILE)
    with lock.acquire(timeout=timeout):
        if verbose:
            print("  Installing web driver...")
        if CHROME_VERSION is not None:
            chromium_exe = get_chromium_exe()
            if verbose:
                print("  Finished installing web driver: ", chromium_exe)
        cache_manager = DriverCacheManager(
            root_dir=WDM_DIR, valid_range=CACHE_TIMEOUT_DAYS
        )
        # opts.binary_location = chromium_exe
        driver_path = ChromeDriverManager(
            cache_manager=cache_manager, driver_version=CHROME_VERSION
        ).install()
    if verbose:
        print(f"\n  Using ChromeDriver: {driver_path}")
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        driver = webdriver.Chrome(options=opts)  # , service_log_path=LOG_FILE)
        if headless:
            driver.set_window_size(1440, 900)
        return driver
    except Exception as err:  # pylint: disable=broad-except
        traceback.print_exc()
        log_file_text = ""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, encoding="utf-8", mode="r") as filed:
                log_file_text = filed.read()
        print(f"{__file__}: Error: {err}")
        print(f"{LOG_FILE}:\n{log_file_text}")
        raise


if __name__ == "__main__":
    open_webdriver()
