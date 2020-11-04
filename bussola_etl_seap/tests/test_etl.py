"""Tests for SEAP ETL modules."""
# pylint: disable=redefined-outer-name,singleton-comparison

import datetime
import os
import time
from getpass import getpass
import log

from ..bussola_etl_seap import SEAPBulletin


log.reset()
log.init(verbosity=2)


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.dirname(os.path.dirname(TEST_DIR)) + '/data'
INPUT_DIR = DATA_DIR + '/input'
OUTPUT_DIR = DATA_DIR + '/output'
EXAMPLE_FILE_PATH = INPUT_DIR + '/example.xlsx'

ANVIL_TOKEN = os.environ.get('ANVIL_TOKEN')
if ANVIL_TOKEN is None:
    ANVIL_TOKEN = getpass('Please provide an anvil API token: ')

def test_extract_localfile():
    """Tests whether extraction from local XLSX file is working as expected"""
    bulletin = SEAPBulletin(EXAMPLE_FILE_PATH, date='2020-08-11')
    assert bulletin.tables['facilities'].at[8, 'unidadeNome'] == (
        'Presídio Alfredo Tranjan'
    )

def test_date_parsing():
    """Tests parsing date from file"""
    bulletin = SEAPBulletin(EXAMPLE_FILE_PATH)
    assert bulletin.date.date() == datetime.date(2020, 8, 11)

def test_to_csv():
    """Tests exporting bulletin to local CSV file"""
    start = time.time()
    bulletin = SEAPBulletin(EXAMPLE_FILE_PATH, date='2020-08-11')
    bulletin.to_file(
        output_file=OUTPUT_DIR + '/[YYYY][MM][DD]_SEAPRJ.csv',
        tablename='facilities'
    )
    expected_results = [
        OUTPUT_DIR + '/20200811_SEAPRJ_facilities.csv',
    ]
    for _file in expected_results:
        # check there is a file in the expected path
        log.info(f"Checking whether {_file} exists...")
        assert os.path.isfile(_file)
        # check file was updated in this test (is not a preexisting file)
        log.info(f"Checking wheter {_file} was updated...")
        assert os.path.getmtime(_file) >= start

def test_to_json():
    """Tests exporting bulletin to local CSV file"""
    start = time.time()
    bulletin = SEAPBulletin(EXAMPLE_FILE_PATH, date='2020-08-11')
    bulletin.to_file(
        output_file=OUTPUT_DIR + '/[YYYY][MM][DD]_SEAPRJ.json',
        tablename='facilities'
    )
    expected_results = [
        OUTPUT_DIR + '/20200811_SEAPRJ_facilities.json',
    ]
    for _file in expected_results:
        # check there is a file in the expected path
        log.info(f"Checking whether {_file} exists...")
        assert os.path.isfile(_file)
        #assert _file in os.listdir(OUTPUT_DIR)
        # check file was updated in this test (is not a preexisting file)
        log.info(f"Checking whether {_file} was updated...")
        assert os.path.getmtime(_file) >= start

def test_to_anvil():
    """Test exporting to an Anvil app"""
    bulletin = SEAPBulletin(EXAMPLE_FILE_PATH, date='2020-08-11')
    assert bulletin.to_anvil(
        tablename='occupation',
        output_table='bsp_seap_ocupacao',
        token=ANVIL_TOKEN,
    )
