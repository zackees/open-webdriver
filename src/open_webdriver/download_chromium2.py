import json
import os
import platform
import shutil
import sys
import zipfile

from download import download  # pip install download

from open_webdriver.path import WDM_DIR

# Chromium snapshot URLs per platform
BASE_URL = "https://commondatastorage.googleapis.com/chromium-browser-snapshots"

PLATFORM_MAP = {
    "Windows": ("Win_x64", "chrome-win", "chrome.exe"),
    "Linux": ("Linux_x64", "chrome-linux", "chrome"),
    "Darwin": ("Mac", "chrome-mac", "Chromium.app/Contents/MacOS/Chromium"),
}


def get_latest_revision(platform_id: str) -> str:
    url = f"{BASE_URL}/{platform_id}/LAST_CHANGE"
    import httpx

    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.text.strip()


def get_cache_file(system: str) -> str:
    return os.path.join(WDM_DIR, f".chromium-info-{system}.json")


def is_chromium_cached(system: str, revision: str, exe_path: str) -> bool:
    cache_file = get_cache_file(system)
    if not os.path.exists(cache_file):
        return False
    try:
        with open(cache_file, "r") as f:
            data = json.load(f)
            return data.get("revision") == revision and os.path.exists(exe_path)
    except Exception:
        return False


def write_cache(system: str, revision: str, exe_path: str):
    cache_file = get_cache_file(system)
    data = {"revision": revision, "executable": exe_path}
    with open(cache_file, "w") as f:
        json.dump(data, f)


def download_and_extract_chromium() -> str:
    system = platform.system()
    if system not in PLATFORM_MAP:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    platform_id, folder_name, binary_path = PLATFORM_MAP[system]
    revision = get_latest_revision(platform_id)
    extract_dir = os.path.join(WDM_DIR, f"chromium-{system}")
    executable_path = os.path.join(extract_dir, folder_name, binary_path)

    if is_chromium_cached(system, revision, executable_path):
        print(f"✅ Chromium already installed (rev {revision}) at:")
        print(f"▶ {executable_path}")
        return executable_path

    zip_url = f"{BASE_URL}/{platform_id}/{revision}/{folder_name}.zip"
    zip_path = os.path.join(WDM_DIR, f"{folder_name}.zip")

    print(f"⬇ Downloading Chromium rev {revision} from: {zip_url}")
    download(zip_url, zip_path, replace=True)

    # Clean and extract
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    os.remove(zip_path)

    write_cache(system, revision, executable_path)

    print("\n✅ Chromium downloaded and extracted!")
    print(f"▶ Path to Chromium binary: {executable_path}")
    return executable_path


def find_chromium_in_paths() -> str | None:
    """Search for Chromium in common system paths."""
    system = platform.system()
    if system not in PLATFORM_MAP:
        return None

    _, _, binary_name = PLATFORM_MAP[system]
    # Get just the executable name without folder path
    binary_name = os.path.basename(binary_name)

    search_paths = []
    if system == "Windows":
        program_files = [
            os.environ.get("PROGRAMFILES", "C:\\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
        ]
        for pf in program_files:
            search_paths.extend(
                [
                    os.path.join(pf, "Chromium", binary_name),
                    os.path.join(pf, "Google", "Chrome", binary_name),
                ]
            )
    elif system == "Darwin":
        search_paths.extend(
            [
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ]
        )
    elif system == "Linux":
        search_paths.extend(
            ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]
        )

    for path in search_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def _set_exe_permissions(exe_path: str) -> None:
    if platform.system() == "Windows":
        return

    os.chmod(exe_path, 0o755)
    if platform.system() == "Darwin":
        # Remove quarantine attribute
        os.system(f"xattr -d com.apple.quarantine {exe_path}")


def get_chromium_exe() -> str:
    """Fetches the Chromium executable path."""
    # First check if Chromium exists in system paths
    system_chromium = find_chromium_in_paths()
    if system_chromium:
        print("✅ Found existing Chromium installation at:")
        print(f"▶ {system_chromium}")
        return system_chromium

    # If not found in system paths, download it
    exe_path = download_and_extract_chromium()
    if not os.path.exists(exe_path):
        print(f"❌ Chromium executable not found: {exe_path}")
        sys.exit(1)

    # add permissions
    _set_exe_permissions(exe_path)
    return exe_path


if __name__ == "__main__":
    download_and_extract_chromium()
