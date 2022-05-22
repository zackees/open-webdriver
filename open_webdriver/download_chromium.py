"""
Module to download the Chromium browser from the repo.
"""

import os
import sys

from download import download  # type: ignore

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def get_chromium_exe() -> str:
    """Run the unit tests."""
    url_src = f"https://github.com/zackees/open-webdriver/raw/main/chromium/{sys.platform}.zip"
    dir_dst = os.path.join(ROOT, ".wdm", "chromium")
    os.makedirs(dir_dst, exist_ok=True)
    download(url=url_src, path=dir_dst, kind="zip", progressbar=True, replace=False)
    platform_dir = os.path.join(dir_dst, sys.platform)
    if sys.platform == "win32":
        exe_path = os.path.join(platform_dir, "chrome.exe")
    elif sys.platform == "linux":
        exe_path = os.path.join(platform_dir, "chromium")
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")
    assert os.path.exists(exe_path), f"Chromium executable not found: {exe_path}"
    return exe_path


if __name__ == "__main__":
    get_chromium_exe()
