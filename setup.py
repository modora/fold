from setuptools import setup, find_packages

setup(
    name="fold",
    version="21.12.0",
    packages=["fold", "fold.core"],
    install_requires=[
        "loguru",
        "pyfunctional",
        "toml",
        "pyyaml",
    ],
)
