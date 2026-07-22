import click

@click.group()
def cli():
    """
    snipcli is a command-line tool for managing code snippets.
    """
    pass

if __name__ == '__main__':
    cli()