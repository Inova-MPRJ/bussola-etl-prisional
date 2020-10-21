#!/usr/bin/env python

"""Package entry point."""


from . import bussola_etl_seap
from .cli import etl


if __name__ == '__main__':  # pragma: no cover
    etl()
