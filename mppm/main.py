import click
from build import ProjectBuilder
from resolvelib import BaseReporter, Resolver

import subprocess

from .env import MppmEnv
from .locker import Locker
from .provider import Provider
from .pyproject import PyProjectToml

toml = PyProjectToml()

@click.group()
def cli():
    pass

@click.command()
def lock():
    dependencies = toml.get_mppm_dependencies()
    python_version = toml.get_python_version()
    resolver = Resolver(Provider(python_version), BaseReporter())

    click.echo("//---dependencies---")
    click.echo(dependencies)
    click.echo("//---python version---")
    click.echo(python_version)
    click.echo("//---resolver result---")
    resolve_dependencies_result = resolver.resolve(dependencies)
    Locker.lock(resolve_dependencies_result.mapping)
    click.echo("//---[lock done!]---")
    for k, v in resolve_dependencies_result.mapping.items():
        click.echo(f"{k} = {v.version}")

@click.command()
def install():
    dependencies = Locker.read()
    python_version = toml.get_python_version()
    MppmEnv.create(python_version)
    for _, v in dependencies.items():
        # assume only wheel file. Wheel can be installed by .whl URL.
        MppmEnv.install(v['url'])

    click.echo("//---[install done!]---")

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
