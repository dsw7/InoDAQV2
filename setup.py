from setuptools import setup, find_packages

setup(
    name="InoDAQV2",
    version="1.1",
    package_data={"inodaqv2": ["templates/*", "static/*js"]},
    packages=find_packages(),
    install_requires=[
        "click",
        "flask",
        "inoio",
    ],
    entry_points={"console_scripts": ["inodaq = inodaqv2.main:main"]},
)
