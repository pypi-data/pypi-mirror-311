from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="win11_notificationbar",
    version="0.0.2",
    author="UF4",
    author_email="uf4hp@foxmail.com",
    description="win11_notificationbar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)