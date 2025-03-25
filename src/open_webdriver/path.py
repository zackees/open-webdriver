"""
Paths for the project.
"""

import os
import sys

ROOT = os.path.dirname(sys.argv[0])
WDM_DIR = os.path.join(ROOT, ".wdm")
WDM_CHROMIUM_DIR = os.path.join(WDM_DIR, "chromium")
LOG_FILE = os.path.join(WDM_DIR, "open_webdriver.log")
