import click

from .pyproject import PyProjectToml

toml = PyProjectToml()

@click.group()
def cli():
    pass

@click.command()
def lock():
    dependencies = toml.get_mppm_dependencies()
    python_version = toml.get_python_version()
    click.echo("//---dependencies---")
    click.echo(dependencies)
    click.echo("//---python version---")
    click.echo(python_version)

@click.command()
def install():
    click.echo('install!')

@click.command()
@click.argument('args', nargs=-1)
def run(args):
    click.echo(f'{list(args)}')

cli.add_command(lock)
cli.add_command(install)
cli.add_command(run)
