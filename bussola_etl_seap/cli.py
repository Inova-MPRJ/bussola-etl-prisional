"""A sample CLI."""

import click
import log

# from . import utils
from typing import Optional


@click.command()
@click.argument('input')
@click.argument('output')
def main(input: Optional[str] = None, output: Optional[str] = None) -> None:
    log.init()

    if input is not None:
        pass

    message = 'Este módulo está em construção!'
    click.echo(message)


if __name__ == '__main__':  # pragma: no cover
    main()
