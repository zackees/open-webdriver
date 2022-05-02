# open-webdriver

[![Actions Status](https://github.com/zackees/open-webdriver/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_macos.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Win_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_win.yml)
[![Actions Status](https://github.com/zackees/open-webdriver/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/open-webdriver/actions/workflows/test_ubuntu.yml)

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

# Changes
  * 1.0.4: Now pins dependencies.
  * 1.0.0: Initial code submit.
