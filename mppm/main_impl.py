import click
from resolvelib import BaseReporter, Resolver
from typing import Dict, Optional, Any, List
from packaging.requirements import Requirement


from .env import MppmEnv
from .locker import Locker
from .provider import Provider
from .pyproject import PyProjectToml


def install_impl(toml: Optional[PyProjectToml] = None) -> None:
    if toml is None:
        toml = PyProjectToml()
    dependencies: Dict[str, Any] = Locker.read()
    python_version: str = toml.get_python_version()
    MppmEnv.create(python_version)
    for _, v in dependencies.items():
        # assume only wheel file. Wheel can be installed by .whl URL.
        MppmEnv.install(v['url'])

    click.echo("//---[install done!]---")

def lock_impl(toml: Optional[PyProjectToml] = None) -> None:
    if toml is None:
        toml = PyProjectToml()
    dependencies: List[Requirement] = toml.get_mppm_dependencies()
    python_version: str = toml.get_python_version()
    resolver: Resolver = Resolver(Provider(python_version), BaseReporter())

    click.echo("//---dependencies---")
    click.echo(dependencies)
    click.echo("//---python version---")
    click.echo(python_version)
    click.echo("//---resolver result---")
    try:
        resolve_dependencies_result = resolver.resolve(dependencies)
        Locker.lock(resolve_dependencies_result.mapping)
        click.echo("//---[lock done!]---")
        for k, v in resolve_dependencies_result.mapping.items():
            click.echo(f"{k} = {v.version}")
    except:
        click.echo(f"Failed to resolve dependencies")