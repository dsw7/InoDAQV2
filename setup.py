from setuptools import setup, find_packages

setup(
    name="InoDAQV2",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "inoio",
    ],
    entry_points={
        "console_scripts": [
            "inodaq = gui.main:main",
        ]
    },
)
