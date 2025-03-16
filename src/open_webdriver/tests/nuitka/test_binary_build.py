"""
Demo app build in nuitka. This builds a single file binary which is self signed and
can be distributed. To build for a platform, you must have that platform. So Windows
can build for win32 platform, MacOS for darwin and Linux for Linux.
"""

# pylint: disable=R1716

import os
import subprocess
import sys
import zipfile
from pprint import pprint

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
APP_SRC = os.path.join(PROJECT_ROOT, "src", "open_webdriver", "demo_app.py")
DEFAULT_APP_BUILD_DIR = os.path.join(
    PROJECT_ROOT, "tests", "nuitka", "test_data", "build", "demo_app"
)
APP_BUILD_DIR = os.environ.get("RUNNER_TEMP", DEFAULT_APP_BUILD_DIR)  # gh_actions


def main() -> int:
    """Builds the demo app."""
    app_name = "open_webdriver.demo_app"
    if sys.platform == "win32":
        app_name += ".exe"
    app_exe_out = os.path.join(APP_BUILD_DIR, app_name)

    print("os.environ:")
    pprint(dict(os.environ))

    print(f"Changing directory to {PROJECT_ROOT}")
    os.chdir(PROJECT_ROOT)

    cmd_list = [
        "uv pip install -r requirements.nuitka.txt",
        "&&",
        "uv pip install -e .",
        "&&",
        "uv run -m nuitka",
        "--assume-yes-for-downloads",
        "--follow-imports",
        "--standalone",
        "--python-flag=-OO",  # Strips comments
        "--include-package-data=selenium",  # For html/js/css resources
        f"--output-dir={APP_BUILD_DIR}",
        APP_SRC,
        "--onefile",
        "-o",
        app_name,
    ]
    cmd_str = " ".join(cmd_list)

    print(f"Executing:\n  {cmd_str}")
    rtn = os.system(cmd_str)

    if rtn != 0:
        print("Failed to build")
        sys.exit(rtn)
    print(f"Successfully built {os.path.join(APP_BUILD_DIR, app_name)}")

    assert os.path.exists(APP_BUILD_DIR), f"No directory: {APP_BUILD_DIR}"
    os.chdir(APP_BUILD_DIR)

    # make a zip file of the app_name at the current directory
    with zipfile.ZipFile(f"{app_name}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(app_name)

    expected_zip_file = os.path.join(APP_BUILD_DIR, f"{app_name}.zip")
    assert os.path.isfile(expected_zip_file)
    assert os.path.isfile(app_exe_out)

    os.chmod(app_exe_out, 0o755)  # Execution permissions.

    print(
        f'\nDone building app "{app_name}", binary located at:\n  {os.path.abspath(app_name)}\n'
    )
    print(
        "***************************\n"
        f"Running\n  {app_exe_out}\n"
        "***************************"
    )

    try:
        subprocess.run(app_exe_out, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        print(
            f"Failed to run app, return code was {err.returncode}\n  output was:\n{err.output}\n  stderr was:\n{err.stderr}"
        )
        sys.exit(err.returncode)

    print(f"Output of running binary {app_exe_out} was successful")
    return 0


if __name__ == "__main__":
    sys.exit(main())
