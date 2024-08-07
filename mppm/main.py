import subprocess
from typing import Callable, List, Tuple

import click
from build import ProjectBuilder
from resolvelib import BaseReporter, Resolver

from .env import MppmEnv
from .locker import Locker
from .main_impl import install_impl, lock_impl
from .provider import Provider
from .pyproject import PyProjectToml


@click.group()  # type: ignore
def cli() -> None:
    pass

@click.command()  # type: ignore
def lock() -> None:
    lock_impl()

@click.command()  # type: ignore
def install() -> None:
    install_impl()

@click.command()  # type: ignore
@click.argument('args', nargs=-1)  # type: ignore
def run(args: Tuple[str, ...]) -> None:
    MppmEnv.run(list(args))

@click.command()  # type: ignore
def build() -> None:
    builder: ProjectBuilder = ProjectBuilder(".", ".mppmenv/bin/python")
    for x in builder.build_system_requires:
        MppmEnv.install(x)
    builder.build("wheel", "dist")

@click.command()  # type: ignore
def publish() -> None:
    target_repository_hosted_site: str = "testpypi"  # testpypi or pypi
    subprocess.run(
        ["twine", "upload", "--repository", target_repository_hosted_site, "dist/*"],
        check=True
    )

cli.add_command(lock)
cli.add_command(install)
cli.add_command(run)
cli.add_command(build)
cli.add_command(publish)