import os
from pathlib import Path

from setuptools import Extension, find_namespace_packages, setup

PROJECT_ROOT = Path(__file__).parent
long_description = (PROJECT_ROOT / "README.md").read_text(encoding="utf8")

setup(
    name="pyinstrument",
    packages=find_namespace_packages(include=["pyinstrument*"]),
    version="4.6.2",
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
    extras_require={
        "test": [
            "pytest",
            "flaky",
            "trio",
            "cffi >= v1.17.0rc1 ; python_version >= '3.13'",  # trio dep, pinned to a version that works with py3.13
            "greenlet>=3.0.0a1 ; python_version < '3.13'",
            "greenlet @ https://github.com/vstinner/greenlet/archive/refs/heads/py313.zip ; python_version >= '3.13'",
            "pytest-asyncio==0.12.0",  # pinned to an older version due to an incompatibility with flaky
            "ipython",
        ],
        "bin": [
            "click",
            "nox",
        ],
        "docs": [
            "sphinx==7.4.7",
            "myst-parser==3.0.1",
            "furo==2024.7.18",
            "sphinxcontrib-programoutput==0.17",
            "sphinx-autobuild==2024.4.16",
        ],
        "examples": [
            "numpy",
            "django",
        ],
        "types": [
            "typing_extensions",
        ],
    },
    include_package_data=True,
    python_requires=">=3.8",
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
