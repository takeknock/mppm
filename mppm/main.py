import click

@click.group()
def cli():
    pass

@click.command()
def lock():
    click.echo('lock!')

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
