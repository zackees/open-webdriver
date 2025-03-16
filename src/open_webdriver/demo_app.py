"""
Demo app to open up a webdriver to a website then close.
"""

from open_webdriver.main import open_webdriver


def main() -> None:
    """Simple main to open up a webdriver to a website then close."""
    print("Openning webdriver")
    with open_webdriver(headless=False) as driver:
        driver.get("https://www.google.com")
    print("Webdriver closed successfully")


if __name__ == "__main__":
    main()
