import os

import nox

nox.needs_version = ">=2024.4.15"
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"])
def test(session):
    session.env["UV_PRERELEASE"] = "allow"
    session.install("-e", ".[test]")
    session.run("pytest")
