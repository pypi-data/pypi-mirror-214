import requests
from setuptools import find_packages, setup


def versions(package_name: str) -> str:
    data = requests.get(f"https://pypi.python.org/pypi/{package_name}/json")
    _versions = data.json()["releases"].keys()
    return list(_versions)[-1]


package_version = versions("novalabs-backtest")
VERSION = package_version[:-1] + str(int(package_version[-1]) + 1)

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="novalabs-backtest",
    version="1.1.27",
    author="Nova Labs",
    author_email="devteam@novalabs.ai",
    description="Wrappers around Nova Labs utilities focused on safety and testability.",
    long_description=long_description,
    url="https://github.com/Nova-DevTeam/nova-backtest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
)
