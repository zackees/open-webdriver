"""
    Handles the creation of the web driver.
"""

# pylint: disable=protected-access

import os
import ssl
import sys
from typing import Any

import urllib3  # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver import ChromeOptions  # type: ignore
from selenium.webdriver import FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from webdriver_manager.driver import Driver  # type: ignore
from webdriver_manager.firefox import GeckoDriverManager  # type: ignore

urllib3.disable_warnings()

ssl._create_default_https_context = ssl._create_unverified_context

# Turn off SSL verification to allow visiting websites with self-signed certs.
os.environ["WDM_SSL_VERIFY"] = "0"
if "WDM_LOCAL" not in os.environ:
    os.environ["WDM_LOCAL"] = "1"

FORCE_HEADLESS = sys.platform == "linux" and "DISPLAY" not in os.environ
DEFAULT_DRIVER = "chrome"

CACHE_TIMEOUT = 7

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(os.path.dirname(HERE), "open_webdriver.log")


def open_webdriver(
    driver_name: str = DEFAULT_DRIVER,
    headless: bool = True,
    verbose: bool = False,  # pylint: disable=unused-argument
) -> Driver:
    """Opens the web driver."""

    # Hack for windows. This is needed or else web-driver will fail to start
    # and report a very strange error that it can't find the binary. This
    # seems to happen ONLY in tox spawned tests.
    if sys.platform == "win32":
        os.environ.setdefault("PROGRAMW6432", "C:\\Program Files")

    opts: Any = None

    if headless or FORCE_HEADLESS:
        if FORCE_HEADLESS and not headless:
            print("\n  WARNING: HEADLESS ENVIRONMENT DETECTED, FORCING HEADLESS")
        headless = True
    if driver_name in ["chrome"]:
        # For Chrome/Brave just install the driver immediately.
        opts = ChromeOptions()
        opts.add_argument("--ignore-certificate-errors")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        if headless:
            opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")
        driver_path = ChromeDriverManager(cache_valid_range=CACHE_TIMEOUT).install()
        if verbose:
            print(f"\n  Using ChromeDriver: {driver_path}")
        return webdriver.Chrome(driver_path, options=opts, service_log_path=LOG_FILE)
    if driver_name == "firefox":
        print(f"{__file__}: Warning: firefox browser has known issues.")
        opts = FirefoxOptions()
        opts.accept_insecure_certs = True
        if headless:
            opts.headless = True
        driver_path = GeckoDriverManager(cache_valid_range=CACHE_TIMEOUT).install()
        if verbose:
            print(f"\n  Using FirefoxDriver: {driver_path}")
        return webdriver.Firefox(executable_path=driver_path, options=opts, log_path=LOG_FILE)
    raise NotImplementedError(
        f"Unsupported driver name: {driver_name}. Supported drivers: chrome, firefox."
    )
    # Don't spam the console with warnings.
    # try:
    #     if not verbose:
    #         logging.captureWarnings(True)
    #     driver = get_webdriver_for(browser=driver_name, options=opts)
    # finally:
    #     if not verbose:
    #         logging.captureWarnings(False)
    # return driver
