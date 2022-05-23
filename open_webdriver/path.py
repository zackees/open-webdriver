"""
Paths for the project.
"""

import os

ROOT = os.path.dirname(os.path.dirname(__file__))
os.chdir(ROOT)
ROOT = os.path.relpath(ROOT, ".")
WDM_DIR = os.path.join(ROOT, ".wdm")
WDM_CHROMIUM_DIR = os.path.join(WDM_DIR, "chromium")
LOG_FILE = os.path.join(ROOT, "open_webdriver.log")
WDM_DIR = os.path.join(ROOT, ".wdm")
