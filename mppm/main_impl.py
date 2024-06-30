import click
from resolvelib import BaseReporter, Resolver


from .env import MppmEnv
from .locker import Locker
from .provider import Provider
from .pyproject import PyProjectToml


def install_impl(toml=None):
    if toml == None:
        toml = PyProjectToml()
    dependencies = Locker.read()
    python_version = toml.get_python_version()
    MppmEnv.create(python_version)
    for _, v in dependencies.items():
        # assume only wheel file. Wheel can be installed by .whl URL.
        MppmEnv.install(v['url'])

    click.echo("//---[install done!]---")

def lock_impl(toml=None):
    if toml == None:
        toml = PyProjectToml()
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