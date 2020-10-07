"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,singleton-comparison


import pytest

from bussola_etl_seap import bussola_etl_seap as seap


def test_seap_bulletin_v1_constructor():
    input_test = './myfile.xlsx'
    output_test = './myresult.csv'
    with pytest.raises(NotImplementedError):
        seap.SEAPBulletinV1(input_test, output_test)
