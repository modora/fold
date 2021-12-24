from setuptools import setup

setup(
    name="fold",
    version="21.12.1",
    python_requires=">=3.10",
    packages=["fold", "fold.config", "fold.logger", "fold.output"],
    install_requires=[
        "loguru",
        "pyfunctional",
        "toml",
        "pyyaml",
    ],
)
