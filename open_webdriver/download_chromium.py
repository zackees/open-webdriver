"""
Module to download the Chromium browser from the repo.
"""

import os
import sys
import zipfile

from download import download  # type: ignore

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WDM_DIR = os.path.join(ROOT, ".wdm")
WDM_CHROMIUM_DIR = os.path.join(WDM_DIR, "chromium")


def _set_exe_permissions(start_dir: str) -> None:
    """Sets the permissions on the chromium executable."""
    if sys.platform == "win32":
        return
    for root, _, files in os.walk(start_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            os.chmod(path, 0o755)


def get_chromium_exe() -> str:
    """Fetches the chromium executable."""
    url_src = f"https://github.com/zackees/open-webdriver/raw/main/chromium/{sys.platform}.zip"
    platform_dir = os.path.join(WDM_CHROMIUM_DIR, sys.platform)
    finished_stamp = os.path.join(platform_dir, "finished")
    if not os.path.exists(finished_stamp):
        zip_dst = os.path.join(WDM_CHROMIUM_DIR, sys.platform + ".zip")
        download(url=url_src, path=zip_dst, kind="file", progressbar=True, replace=False)
        assert os.path.exists(zip_dst), f"{zip_dst} does not exist."
        with zipfile.ZipFile(zip_dst, "r") as zipf:
            zipf.extractall(WDM_CHROMIUM_DIR)
        _set_exe_permissions(platform_dir)
        # Touch file.
        with open(finished_stamp, encoding="utf-8", mode="w") as filed:
            filed.write("")
        os.remove(zip_dst)
    exe_path = None
    if sys.platform == "win32":
        exe_path = os.path.join(platform_dir, "chrome.exe")
    elif sys.platform == "linux":
        exe_path = os.path.join(platform_dir, "chrome")
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")
    assert os.path.exists(exe_path), f"Chromium executable not found: {exe_path}"
    return exe_path


if __name__ == "__main__":
    print(get_chromium_exe())
