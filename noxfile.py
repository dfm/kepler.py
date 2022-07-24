import nox


@nox.session
def tests(session):
    pass


@nox.session
def build(session):
    pass


@nox.session
def  lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
