import os

import nox

nox.needs_version = ">=2024.4.15"
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"])
def test(session):
    session.env["UV_PRERELEASE"] = "allow"
    session.install("-e", ".[test]", "setuptools")
    session.run("python", "setup.py", "build_ext", "--inplace")
    session.run("pytest")


@nox.session()
def docs(session):
    session.env["UV_PRERELEASE"] = "allow"
    session.install("-e", ".[docs]")
    session.run("make", "-C", "docs", "html")


@nox.session(default=False)
def livedocs(session):
    session.env["UV_PRERELEASE"] = "allow"
    session.install("-e", ".[docs]")
    session.run("make", "-C", "docs", "livehtml")


@nox.session(default=False, python=False)
def htmldev(session):
    with session.chdir("html_renderer"):
        session.run("npm", "install")
        session.run("npm", "run", "dev")


@nox.session(default=False, python=False)
def watchbuild(session):
    # this doesn't use nox's environment isolation, because we want to build
    # the python version of the activated venv
    # we pass --force because the build_ext command doesn't rebuild if the
    # headers change
    session.run("python", "setup.py", "build_ext", "--inplace", "--force")
    session.run(
        "pipx",
        "run",
        "--spec",
        "watchdog",
        "watchmedo",
        "shell-command",
        "--patterns=*.h;*.c;setup.py;setup.cfg",
        "--recursive",
        "--command=python setup.py build_ext --inplace --force",
        "pyinstrument",
    )


@nox.session(python=False, default=False)
def watch(session):
    session.run(
        "npx",
        "concurrently",
        "--kill-others",
        "--names",
        "bext,html,docs",
        "--prefix-colors",
        "bgBlue,bgGreen,bgMagenta",
        "nox -s watchbuild",
        "nox -s htmldev",
        "nox -s livedocs",
    )
