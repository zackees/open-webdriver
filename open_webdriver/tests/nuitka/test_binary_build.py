"""
    Demo app build in nuitka. This builds a single file binary which is self signed and
    can be distributed. To build for a platform, you must have that platform. So Windows
    can build for win32 platform, MacOS for darwin and Linux for Linux.
"""

# pylint: disable=R1716

import os
import sys
import zipfile
from pprint import pprint

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
APP_SRC = os.path.join(PROJECT_ROOT, "open_webdriver", "demo_app.py")
DEFAULT_APP_BUILD_DIR = os.path.join(
    PROJECT_ROOT, "tests", "nuitka", "test_data", "build", "demo_app"
)
APP_BUILD_DIR = os.environ.get("RUNNER_TEMP", DEFAULT_APP_BUILD_DIR)  # gh_actions
APP_PACKAGE = "open_webdriver.demo_app"
APP_NAME = "open_webdriver.demo_app"
if sys.platform == "win32":
    APP_NAME += ".exe"
APP_EXE_OUT = os.path.join(APP_BUILD_DIR, APP_NAME)

print("os.environ:")
pprint(dict(os.environ))

print(f"Changing directory to {PROJECT_ROOT}")
os.chdir(PROJECT_ROOT)

CMD = [
    "pip install -r requirements.nuitka.txt",
    "&&",
    "pip install -e .",
    "&&",
    "python -m nuitka",
    "--assume-yes-for-downloads",
    "--follow-imports",
    "--standalone",
    "--python-flag=-OO",  # Strips comments
    "--include-package-data=selenium",  # For html/js/css resources
    f"--output-dir={APP_BUILD_DIR}",
    APP_SRC,
    "--onefile",
    "-o",
    APP_NAME,
]
CMD_STR = " ".join(CMD)

print(f"Executing:\n  {CMD_STR}")
rtn = os.system(CMD_STR)

if rtn != 0:
    print("Failed to build")
    sys.exit(rtn)
print(f"Successfully built {os.path.join(APP_BUILD_DIR, APP_NAME)}")

assert os.path.exists(APP_BUILD_DIR), f"No directory: {APP_BUILD_DIR}"
os.chdir(APP_BUILD_DIR)

# make a zip file of the APP_NAME at the current directory
with zipfile.ZipFile(f"{APP_NAME}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(APP_NAME)

expected_zip_file = os.path.join(APP_BUILD_DIR, f"{APP_NAME}.zip")
assert os.path.isfile(expected_zip_file)
assert os.path.isfile(APP_EXE_OUT)

os.chmod(APP_EXE_OUT, 0o755)  # Execution permissions.

print(f'\nDone building app "{APP_NAME}", binary located at:\n  {os.path.abspath(APP_NAME)}\n')
print("***************************\n" f"Running\n  {APP_EXE_OUT}\n" "***************************")
rtn_code = os.system(APP_EXE_OUT)
assert rtn_code == 0, f"Failed to run app, return code was {rtn_code}"

print(f"Output of running binary {APP_EXE_OUT} was successful")
