# open-webdriver

## The simplest and easiest way to get a selenium webdriver

#### Platform Unit Tests
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu.yml)

#### Platform binary nuitka build
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos_nuitka.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win_nuitka.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_nuitka.yml)

#### Ubuntu Install Tests
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Test_Install/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_install.yml)


# Install

`python -m pip install open-webdriver`

# Api

```python
from open_webdriver import open_webdriver

with open_webdriver(headless=False) as driver:
    driver.get("https://www.google.com")
    assert driver.title == "Google"
```

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

# Version

Chromium uses version: 101.0.4951.64-1


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
