import os
from pathlib import Path

from setuptools import Extension, find_namespace_packages, setup

PROJECT_ROOT = Path(__file__).parent
long_description = (PROJECT_ROOT / "README.md").read_text(encoding="utf8")

setup(
    name="pyinstrument",
    packages=find_namespace_packages(include=["pyinstrument*"]),
    version="4.5.1",
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
    extras_require={"jupyter": ["ipython"]},
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
