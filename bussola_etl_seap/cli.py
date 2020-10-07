"""A sample CLI."""

import click
import log

# from . import utils


@click.command()
@click.argument('input', default="", type=click.Path(exists=False))
@click.argument('output', default="", type=click.Path(exists=False))
def main(input: str, output: str) -> None:
    log.init()

    message = 'Este módulo está em construção!'
    click.echo(message)


if __name__ == '__main__':  # pragma: no cover
    main()
