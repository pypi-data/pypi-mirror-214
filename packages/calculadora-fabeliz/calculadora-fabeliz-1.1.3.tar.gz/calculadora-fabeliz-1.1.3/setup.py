import setuptools
from pathlib import Path


long_desc = Path("README.md").read_text()

setuptools.setup(
    name="calculadora-fabeliz",
    version="1.1.3",
    description="Calculadora Matematica / Math Calculator",
    author='Fabeliz Irene Alvarez Salazar',
    author_email='irenex2018@gmail.com',
)
