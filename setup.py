
"""
Setup file.
"""



from setuptools import setup

URL = "https://github.com/zackees/open-webdriver"


if __name__ == "__main__":
    setup(
        maintainer="Zachary Vorhies",
        url=URL,
        package_data={"": ["assets/example.txt"]},
        include_package_data=True)

