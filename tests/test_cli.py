"""Sample integration test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned


import click.testing.CliRunner
import pytest

from bussola_etl_seap.cli import main


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_main():
    result = runner().invoke(main)
    assert result.exit_code == 0
    assert result.output == 'Este módulo está em construção!'
