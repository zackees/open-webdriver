# open-webdriver

## Platform Unit Tests
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu.yml)

## Platform binary nuitka build
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos_nuitka.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win_nuitka.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Nuitka/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu_nuitka.yml)

# About

The simplest and most production-ready selenium webdriver wrapper API in python.

All the other api-wrappers are under tested and break as soon as they are thrown into a headless
production server. This project aims to make something that's easy to develop and safe.

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

In your build command.

# Changes
  * 1.1.0: Platform binary builds using nuitka are now tested.
  * 1.0.4: Now pins dependencies.
  * 1.0.0: Initial code submit.
