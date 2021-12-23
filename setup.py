from setuptools import setup

setup(
    name="fold",
    version="21.12.0",
    python_requires=">=3.10",
    packages=["fold", "fold.core", "fold.config", "fold.output", "fold.utils"],
    install_requires=[
        "loguru",
        "pyfunctional",
        "toml",
        "pyyaml",
    ],
)
