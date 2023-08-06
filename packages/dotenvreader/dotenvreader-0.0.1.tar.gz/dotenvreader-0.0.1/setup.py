from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as file:
    long_description = "\n" + file.read()

VERSION = "0.0.1"
DESCRIPTION = "Read dotenv files with python"
LONG_DESCRIPTION = "A Package that allows reading with DotENV"

setup(
    name="dotenvreader",
    version=VERSION,
    author="ContentGamer",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["colorama"],
    keywords=["dotenv", ".env", "python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix"
    ]
)