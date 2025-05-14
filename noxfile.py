import nox

nox.options.default_venv_backend = "uv|virtualenv"
# для запуска конкретной используйте флаг nox -s <name>
nox.options.sessions = ["ruff", "ruff_format", "mypy"]


@nox.session(reuse_venv=True)
def ruff(session: nox.Session) -> None:
    session.install(".[dev]")
    session.run("ruff", "check", ".", external=True)


@nox.session(reuse_venv=True)
def ruff_format(session: nox.Session) -> None:
    session.install(".[dev]")
    session.run("ruff", "format", ".", external=True)
    session.run("ruff", "check", "--select", "I", "--fix", ".", external=True)


@nox.session(reuse_venv=True)
def mypy(session: nox.Session) -> None:
    session.install(".[dev]")
    session.run("mypy", ".", "--exclude", "tests/", external=True)


@nox.session(reuse_venv=True)
def tests(session: nox.Session) -> None:
    session.install(".[dev]")
    session.run("pytest", "tests/", external=True)


@nox.session(reuse_venv=True)
def mkdocs(session: nox.Session) -> None:
    """Запускает локальный сервер документации (режим live reload)."""
    session.install(".[dev]")
    session.run("mkdocs", "serve", external=True)


@nox.session(reuse_venv=True)
def mkdocs_deploy(session: nox.Session) -> None:
    """Собирает и деплоит документацию на GitHub Pages."""
    session.install(".[dev]")
    session.run("mkdocs", "gh-deploy", "--clean", external=True)
