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
APP_NAME = os.path.basename(APP_SRC).replace(".py", "")
if sys.platform == "win32":
    APP_NAME += ".exe"
APP_EXE_OUT = f"{APP_BUILD_DIR}/{APP_NAME}"

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
    APP_EXE_OUT,
]
CMD_STR = " ".join(CMD)

print(f"Executing:\n  {CMD_STR}")
rtn = os.system(CMD_STR)

if rtn != 0:
    print("Failed to build")
    sys.exit(rtn)
print(f"Successfully built {APP_BUILD_DIR}")

os.chdir(APP_BUILD_DIR)

# make a zip file of the APP_NAME at the current directory
with zipfile.ZipFile(f"{APP_NAME}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(APP_NAME)

expected_zip_file = f"{APP_BUILD_DIR}/{APP_NAME}.zip"
assert os.path.exists(expected_zip_file)
assert os.path.exists(APP_EXE_OUT)

os.chmod(APP_EXE_OUT, 0o755)  # Execution permissions.

print(f'\nDone building app "{APP_NAME}", binary located at:\n  {os.path.abspath(APP_NAME)}\n')

print(f"Now testing running of binary {APP_EXE_OUT}")

rtn_code = os.system(APP_EXE_OUT)
assert rtn_code == 0, f"Failed to run app, return code was {rtn_code}"

print(f"Output of running binary {APP_EXE_OUT} was successful")
