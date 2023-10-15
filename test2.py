import click
import functools

@click.group()
def cli():
    pass

def common_options(f):
    options = [
        click.option("-a", is_flag=True),
        click.option("-b", is_flag=True),
    ]
    return functools.reduce(lambda x, opt: opt(x), options, f)

@cli.command()
@common_options
def hello(**kwargs):
    print(kwargs)
    # to get the value of b:
    print(kwargs["b"])

@cli.command()
@common_options
@click.option("-c", "--citrus")
def world(citrus, a, **kwargs):
    print("citrus is", citrus)
    if a:
        print(kwargs)
    else:
        print("a was not passed")

if __name__ == "__main__":
    cli()
