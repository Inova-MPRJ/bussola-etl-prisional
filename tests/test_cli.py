"""Sample integration test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned


from click.testing import CliRunner

from bussola_etl_seap.cli import main


def test_main():
    """Teste da função de entrada da interface de comando"""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert result.output == 'Este módulo está em construção!\n'
