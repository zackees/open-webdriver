"""
    Builds the bigleague site.
"""

# pylint: disable=R1716

import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))

os.chdir(PROJECT_ROOT)

APP_SRC = os.path.join(PROJECT_ROOT, "tests", "nuitka", "test_data", "demo_app.py")
APP_BUILD_DIR = os.path.join(PROJECT_ROOT, "tests", "nuitka", "test_data", "build", "demo_app")
APP_NAME = os.path.basename(APP_SRC).replace(".py", "")
if sys.platform == "win32":
    APP_NAME += ".exe"

APP_EXE_OUT = f"{APP_BUILD_DIR}/{APP_NAME}",
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
    "--include-package-data=selenium",
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

os.chdir(APP_BUILD_DIR)

# make a zip file of the APP_NAME at the current directory
with zipfile.ZipFile(f"{APP_NAME}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(APP_NAME)
    
expected_zip_file = f"{APP_BUILD_DIR}/{APP_NAME}.zip"
assert os.path.exists(expected_zip_file)
assert os.path.exists(APP_EXE_OUT)

print(f'\nDone building app "{APP_NAME}", binary located at:\n  {os.path.abspath(APP_NAME)}\n')

print(f"Now testing running of binary")
assert 0 == os.system(f"{APP_EXE_OUT}")
