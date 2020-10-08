"""Sample integration test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

import sys, os
from click.testing import CliRunner

from bussola_etl_seap.cli import etl


TESTS_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.relpath('../bussola_etl_seap', TESTS_PATH))


def test_etl_localfile():
    """Teste da função de ETL a partir de um arquivo local"""

    runner = CliRunner()
    example_file = os.path.relpath('../data/input/example.xlsx', TESTS_PATH)
    result = runner.invoke(
        etl, [example_file, '--date', '2020-08-11', '--verbosity', 3]
    )
    assert result.exit_code == 0
    assert result.output == example_file  # TO-DO: change assertion
