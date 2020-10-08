"""Tests for SEAP ETL modules."""
# pylint: disable=redefined-outer-name,singleton-comparison

import log

from bussola_etl_seap.bussola_etl_seap import SEAPBulletin


log.init(verbosity=3)


def test_from_localfile():
    """Tests whether extraction from local XLSX file is working as expected"""
    example_filepath = './data/input/example.xlsx'
    bulletin = SEAPBulletin(example_filepath, date='2020-08-11')
    assert bulletin.headcount.at[4, 'unidadeNome'] == (
        'Presídio Milton Dias Moreira -SEAPMM'
    )
