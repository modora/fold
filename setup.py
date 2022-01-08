from setuptools import setup

setup(
    name="fold",
    version="22.01.0",
    python_requires=">=3.10",
    packages=["fold.plugin", "fold.config", "fold.logger", "fold.outputs"],
    install_requires=[
        "loguru",
        "pyfunctional",
        "toml",
        "pyyaml",
    ],
)
