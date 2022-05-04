# open-webdriver

## The simplest and easiest way to get a selenium webdriver

## Platform Unit Tests
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu.yml)

## Platform binary nuitka build
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos_nuitka.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win_nuitka.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_nuitka.yml)

# About

Yet another selenium webdriver wrapper API in python.

This api is tested with github actions and the pain points have been found and smoothed out. For example the webdriver is downloaded and installed on first use. Addiotionally this library has been built to support
the nuitka binary compilation of python. This allows you to make a bot and then distribute just a binary
version to a client.

Benefits:

  * Production ready. Cross platform tests.
  * ssl certs are turned off to reduce errors for many websites.
  * Downloading the proper binary for your platform and stashing it next to the app.
  * Headless by default.
  * Intelligently forces headless in a linux environment without a display card (prevents crash).
  * Platform tests to ensure a stable cross platform experience.
  * Pins to a specific version of selenium driver stack to ensure reproducable behavior.
  * Nuitka Binary Builds for all platforms are tested.

# Install

`python -m pip install open-webdriver`

# Api

```
from open_webdriver import open_webdriver

with open_webdriver() as driver:
    driver.get("https://www.google.com")
    assert driver.title == "Google"
```

# Tests

Just simply run `tox` at the command line and everything should be tested. You may need to install `tox` with `python -m pip tox`.

# Nuitka

This package supports the Nuitka cross compiler to binary app. However to make this work YOU MUST include the package data for selenium or you will get errors about missing javascript files when the program loads. To get around this you'll need to add package data:

`python -m nuitka --include-package-data=selenium ...`

For example see the example build file:
[https://github.com/zackees/open-webdriver/blob/main/tests/nuitka/test_binary_build.py](https://github.com/zackees/open-webdriver/blob/main/tests/nuitka/test_binary_build.py)

# Changes
  * 1.1.2: Suppress certificate warnings.
  * 1.1.1: Update readme.
  * 1.1.0: Platform binary builds using nuitka are now tested.
  * 1.0.4: Now pins dependencies.
  * 1.0.0: Initial code submit.
