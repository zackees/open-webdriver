"""
Module to download the Chromium browser from the repo.
"""

import os
import subprocess
import sys
import zipfile

from download import download  # type: ignore

from open_webdriver.path import WDM_CHROMIUM_DIR


def _set_exe_permissions(start_dir: str) -> None:
    """Sets the permissions on the chromium executable."""
    if sys.platform == "win32":
        return
    for root, _, files in os.walk(start_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            os.chmod(path, 0o755)


def _unzip(zip_path: str) -> None:
    """Unzips a zip file."""

    if sys.platform == "linux":
        print("Linux detected.")
        url = "https://github.com/zackees/open-webdriver/raw/main/chromium/7za"
        dst = os.path.join(WDM_CHROMIUM_DIR, "7za")
        path_7za = download(url=url, path=dst, kind="file", progressbar=True, replace=True)
        path_7za = os.path.abspath(path_7za)
        assert os.path.exists(path_7za), f"{path_7za} does not exist."
        # Add executable permissions.
        os.chmod(path_7za, 0o755)
        print("Using 7za tool")
        try:
            zip_name = os.path.basename(zip_path)
            cmd = f"{path_7za} -y x {zip_name}"
            print(f'Executing: "{cmd}"')
            _ = subprocess.check_output(cmd, cwd=os.path.dirname(zip_path), shell=True)
        except subprocess.CalledProcessError:
            print("Failed to unzip with command line, falling back to python unzip")
    elif sys.platform == "darwin":
        print("MacOS detected.")
        dir_path = os.path.dirname(zip_path)
        os.makedirs(dir_path, exist_ok=True)
        cmd = f'py7zr x "{os.path.abspath(zip_path)}" "{os.path.abspath(dir_path)}"'
        print(f'Executing: "{cmd}"')
        try:
            _ = subprocess.check_output(cmd, cwd=os.path.dirname(zip_path), shell=True)
        except subprocess.CalledProcessError:
            print(f"Failed to un7z with command line {cmd}")
        # Remove quarantine attribute.
        cmd = f'xattr -d com.apple.quarantine "{os.path.abspath(zip_path)}"'
        print(f'Executing: "{cmd}"')
        os.system(cmd)
    else:
        print("Windows detected.")
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.testzip()
            zipf.extractall(os.path.dirname(zip_path))


def get_chromium_exe() -> str:
    """Fetches the chromium executable."""
    ext = ".7z" if sys.platform == "darwin" else ".zip"
    url_src = f"https://github.com/zackees/open-webdriver/raw/main/chromium/{sys.platform}{ext}"
    platform_dir = os.path.join(WDM_CHROMIUM_DIR, sys.platform)
    print(f"WDM_CHROMIUM_DIR: {WDM_CHROMIUM_DIR}")
    finished_stamp = os.path.join(platform_dir, "finished")
    if not os.path.exists(finished_stamp):
        ext = ".7z" if sys.platform == "darwin" else ".zip"
        archive_dst = platform_dir + ext
        print(f"Download {url_src} to {archive_dst}")
        download(url=url_src, path=archive_dst, kind="file", progressbar=True, replace=False)
        assert os.path.exists(archive_dst), f"{archive_dst} does not exist."
        print(f"Unzipping {archive_dst}")
        _unzip(zip_path=archive_dst)
        print(f"Fixing permissions {platform_dir}")
        _set_exe_permissions(platform_dir)
        # Touch file.
        print(f"Touching file: {finished_stamp}")
        os.makedirs(os.path.dirname(finished_stamp), exist_ok=True)
        with open(finished_stamp, encoding="utf-8", mode="w") as filed:
            filed.write("")
        print(f"Removing {archive_dst}")
        os.remove(archive_dst)
    exe_path = None
    if sys.platform == "win32":
        exe_path = os.path.join(platform_dir, "chrome.exe")
    elif sys.platform == "linux":
        exe_path = os.path.join(platform_dir, "chrome")
    elif sys.platform == "darwin":
        exe_path = os.path.join(platform_dir, "Chromium.app", "Contents", "MacOS", "Chromium")
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")
    print(f"Chromium executable: {exe_path}")
    assert os.path.exists(exe_path), f"Chromium executable not found: {os.path.abspath(exe_path)}"
    return exe_path


if __name__ == "__main__":
    print(get_chromium_exe())
