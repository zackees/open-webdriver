# open-webdriver

## The simplest and easiest way to get a scriptable chrome browser running using selenium webdriver.

Note that this package uses a pinned dependency for urllib3 and should be installed in an isolated environment.

# API

```bash
python -m pip install open-webdriver
```

```python
import os
from open_webdriver import open_webdriver
# Needed or else exceptions will be thrown when executed from github actions.
IS_HEADLESS = os.environ.get("GITHUB_ACTIONS") == "true"

def main():
    with open_webdriver(headless=IS_HEADLESS) as driver:
        driver.set_window_size(1440, 900) # Needed for headless mode.
        # All Chromium / web driver dependencies are now installed.
        driver.get("https://www.google.com")
        assert driver.title == "Google"

if __name__ == "__main__":
    main()
```

#### Platform Unit Tests
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos.yml)
[![Win_Tests](https://github.com/zackees/open-webdriver/actions/workflows/test_win.yml/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win.yml)
[![Ubuntu_Tests](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu.yml/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu.yml)

#### Platform binary nuitka build
[![MacOS_Nuitka](https://github.com/zackees/open-webdriver/actions/workflows/test_macos_nuitka.yml/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos_nuitka.yml)
[![Win_Nuitka](https://github.com/zackees/open-webdriver/actions/workflows/test_win_nuitka.yml/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win_nuitka.yml)
[![Ubuntu_Nuitka](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_nuitka.yml/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_nuitka.yml)

#### Ubuntu Install Tests
[![Ubuntu_Test_Install](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_install.yml/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_install.yml)


# Versions

Mac/Windows/Linux all use chromium version 101.0.4951.41
The user agent string will always indicate a Windows client, unless overriden.

# About

Yet another selenium webdriver wrapper API in python, with the aims of being the easist to use with only two lines of code to get running.

Unlike other selenium web driver wrappers, this one **has tests for Windows10/MacOS/Ubuntu platforms**.

One function is provided, `open_webdriver(...)` which takes care of downloading, installing and then running selenium.

Additionally, sane defaults are set, such as headless by default and ssl certs turned off. This code is also tested and examples are provided for use with the nuitka cross compiler, which allows you to create an binary executable. This is great for distributing a compiled binary
for Windows/MacOS/Ubuntu of your selenium bot with all original source code removed, making it impossible to reverse engineer.


`open-webdriver` is built on top of webdriver-manager https://pypi.org/project/webdriver-manager/ library, but with the following changes/fixes:
```python
os.environ['WDM_SSL_VERIFY'] = '0'
```

And other sensible platform specific fixes are applied in order for the selenium driver stack to pass the test suite.

Additionally, a versioned chromium binary is downloaded for Linux & Windows, while whatever Chrome system is used for Mac, due to app signing requirements.

When your app is launched, there will be a side folder name `.wdm` which contain the download of the webdriver used and brawser used. The disk cache for the driver is set for 7 day, after which it will be checked for a new version.

Benefits:

  * Production ready. Cross platform tests.
  * ssl certs are turned off to reduce errors for many websites.
  * Downloading the proper binary for your platform and stashing it next to the app.
  * Headless by default.
  * Intelligently forces headless in a linux environment without a display card (prevents crash).
  * Platform tests to ensure a stable cross platform experience.
  * Pins to a specific version of selenium driver stack to ensure reproducable behavior.
  * Nuitka Binary Builds for all platforms are tested.

Downsides:

  * Only chrome is supported right now.


# Tests

#### Dev:

Just simply run `tox` at the command line and everything should be tested. You may need to install `tox` with `python -m pip tox`.

#### Package Test:

Run `open_webdriver_test` for package tests. This is useful if you are on a server and want to figure out if open_webdriver will be able to be run in
headless mode using the `chrome` driver.

# Docker

Please see `Dockerfile` for requirements for including `open_webdriver` in your Docker app.

Docker is supported in this build. Please see the `Dockerfile` and `docker-compose.yml` for bringup instructions. Simply use `docker-compose up` and then ssh into the docker instance and run `open_webdriver_test` and verify that the test completes normally.

# Nuitka

This package supports the Nuitka cross compiler to binary app. However to make this work YOU MUST include the package data for selenium or you will get errors about missing javascript files when the program loads. To get around this you'll need to add package data:

`python -m nuitka --include-package-data=selenium ...`

For example see the example build file:
[https://github.com/zackees/open-webdriver/blob/main/open_webdriver/tests/nuitka/test_binary_build.py](https://github.com/zackees/open-webdriver/blob/main/open_webdriver/tests/nuitka/test_binary_build.py)

# Pull Requests


Pull requests are welcome for this code base. When you submit your pull request you will need to have the following:
  * New code must have a unit/test.
  * Must pass the linting requirements. Run `tox` (also run on your pull request).

# Changes
  * 1.5.0: Upgraded dependencies. No longer depends on ancient version of urllib.
  * 1.4.5: `Driver` returned from `open_webdriver` is now of WebDriver type instead of one of the base classes. Should help linting.
  * 1.4.4: Fixed nuitka build process with breaking dependencies introduced by python-dotenv 1.0.1
  * 1.4.3: Updated nuitka package and fixed breaking build from urllib3 update.
  * 1.4.2: Prints log if chrome driver fails to launch.
  * 1.4.1: Try and fix failed upload on last version.
  * 1.4.0: Adds default user agent string, fixes running headless mode which uses a different user agent string.
  * 1.3.6: Remove mac m1 runner, which doesn't exist on github
  * 1.3.5: Fixes macOS builds, now uses versioned macOS Chromium.
  * 1.3.4: Fixes nuitka builds that broke with panda's update. Nuitka updated from 0.7.7->1.2.2
  * 1.3.3: Adds user_agent.
  * 1.3.2: Adds disable_dev_shm_usage.
  * 1.3.1: Adds disable gpu.
  * 1.3.0: Concurrent support added for open_webdriver() using a lockfile.
  * 1.2.9: Sets downloaded chromedriver version to 101.0.4951.41
  * 1.2.8: Docker support has been added.
  * 1.2.3: Fix bug in 7za unarchiver path.
  * 1.2.2: 7za unarchiver is now included.
  * 1.2.1: Bug fixes and other improvements that easy deployment.
  * 1.2.0: All platforms supported now. Linux / Win32 now downloads a chromioum browser. Firefox has been removed.
  * 1.1.14: Fixes bugs for `open_webdriver_test` cmd
  * 1.1.10: Adds package test `open_webdriver_test` cmd
  * 1.1.9: Moves tests into package to allow running tests from package.
  * 1.1.8: Minor fixes
  * 1.1.7: Nit readme.
  * 1.1.6: Fixes failing win-tox tests due to missing "PROGRAMW6432" value in os.environ (?!). Brave browser removed as it actually didn't work.
  * 1.1.5: Cert warnings now suppressable with non headless sessions.
  * 1.1.3: Suppress more cert warnings.
  * 1.1.2: Suppress certificate warnings.
  * 1.1.1: Update readme.
  * 1.1.0: Platform binary builds using nuitka are now tested.
  * 1.0.4: Now pins dependencies.
  * 1.0.0: Initial code submit.
