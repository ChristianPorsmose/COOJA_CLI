from setuptools import setup, find_packages

setup(
    name="cooja-cli",
    version="0.1",
    packages=find_packages(), 
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "cooja-cli=cooja_cli.cli:cli",
        ],
    },
)
