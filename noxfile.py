import nox


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    session.install("-r", "requirements-dev.txt")
    session.run("pytest")
