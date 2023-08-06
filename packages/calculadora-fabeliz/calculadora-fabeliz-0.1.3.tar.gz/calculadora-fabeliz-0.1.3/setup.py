import setuptools
from pathlib import Path


long_desc = Path("README.md").read_text()

setuptools.setup(
    name="calculadora-fabeliz",
    version="0.1.3",
    long_description=long_desc
)
