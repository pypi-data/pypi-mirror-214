from setuptools import setup, find_packages

setup(
    name="mctech_actuator",
    version="1.0.3",
    packages=find_packages(
        include=["mctech_actuator*"],
        exclude=["*.test"]
    ),
    install_requires=["log4py", "fastapi"]
)
