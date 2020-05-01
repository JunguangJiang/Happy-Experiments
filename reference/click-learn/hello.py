import click

@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def cli(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)
