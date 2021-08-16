import distutils
import os
import subprocess
import sys

from setuptools import Extension, find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
    name="pyinstrument",
    packages=find_packages(),
    version="4.0.3",
    ext_modules=[
        Extension(
            "pyinstrument.low_level.stat_profile",
            sources=["pyinstrument/low_level/stat_profile.c"],
        )
    ],
    description="Call stack profiler for Python. Shows you why your code is slow!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joe Rickerby",
    author_email="joerick@mac.com",
    url="https://github.com/joerick/pyinstrument",
    keywords=["profiling", "profile", "profiler", "cpu", "time", "sampling"],
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.7",
    entry_points={"console_scripts": ["pyinstrument = pyinstrument.__main__:main"]},
    zip_safe=False,
    classifiers=[
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Testing",
    ],
)
