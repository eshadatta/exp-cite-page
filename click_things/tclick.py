import click
from pathlib import Path

@click.command()
@click.option('--repo', help="path to repo", required=True, type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True, writable=True))
def touch(repo):
    """Print dir if the file exists."""
    click.echo(repo)
if __name__ == '__main__':
    touch()