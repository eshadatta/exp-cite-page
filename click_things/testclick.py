import click
import sys
@click.command()
@click.option('--shout', is_flag=True, default=False)
def cli(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)