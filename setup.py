from setuptools import setup, find_packages

setup(
    name="fold",
    version="21.12.0",
    packages=["fold", "fold.core", "fold.config", "fold.output"],
    install_requires=[
        "loguru",
        "pyfunctional",
        "toml",
        "pyyaml",
    ],
)
