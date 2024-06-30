import click
from build import ProjectBuilder
from resolvelib import BaseReporter, Resolver

import subprocess

from .env import MppmEnv
from .locker import Locker
from .provider import Provider
from .pyproject import PyProjectToml
from .main_impl import install_impl, lock_impl


@click.group()
def cli():
    pass

@click.command()
def lock():
    lock_impl()

@click.command()
def install():
    install_impl()

@click.command()
@click.argument('args', nargs=-1)
def run(args):
    MppmEnv.run(args)

@click.command()
def build():
    builder = ProjectBuilder(".", ".mppmenv/bin/python")
    for x in builder.build_system_requires:
        MppmEnv.install(x)
    builder.build("wheel", "dist")

@click.command()
def publish():
    target_repository_hosted_site = "testpypi" # testpypi or pypi
    subprocess.run(
        ["twine", "upload", "--repository", target_repository_hosted_site, "dist/*"],
        check=True
    )

cli.add_command(lock)
cli.add_command(install)
cli.add_command(run)
cli.add_command(build)
cli.add_command(publish)
