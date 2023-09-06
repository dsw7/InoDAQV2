from setuptools import setup, find_packages

setup(
    name="InoDAQV2",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "pytest",
        "typing-extensions",
    ],
    entry_points={"console_scripts": ["inodaq = inodaqv2.main:main"]},
)
