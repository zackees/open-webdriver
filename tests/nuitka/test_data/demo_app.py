from open_webdriver import open_webdriver


def main() -> None:
    """Simple main to open up a webdriver to a website then close."""
    with open_webdriver() as driver:
        driver.get("https://www.google.com")
