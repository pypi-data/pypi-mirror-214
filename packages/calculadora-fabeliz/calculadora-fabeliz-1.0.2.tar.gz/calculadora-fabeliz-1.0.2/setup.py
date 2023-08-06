import setuptools
from pathlib import Path


long_desc = Path("README.md").read_text()

setuptools.setup(
    name="calculadora-fabeliz",
    version="1.0.2",
    long_description="Calculadora Matematica",
    author='Fabeliz Irene Alvarez Salazar',
    author_email='irenex2018@gmail.com',
)
