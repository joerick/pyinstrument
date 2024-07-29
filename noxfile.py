import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test(session):
    session.install("-r", "requirements-dev.txt")
    session.run("pytest")
