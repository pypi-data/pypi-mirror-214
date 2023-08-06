import setuptools
from pathlib import Path


long_desc = Path("README.md").read_text()

setuptools.setup(
    name="calculadora-fabeliz",
    version="0.0.2",
    long_description=long_desc
)
