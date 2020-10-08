"""Classes that model SEAP bulletins and methods to get info from them"""
# pylint: disable=redefined-outer-name,singleton-comparison

import log
import pandas as pd


class SEAPBulletin:
    """Representation of a weekly bulletin from SEAP"""

    def __init__(self, filepath, date: str = None):
        self.original_file = filepath
        if date is not None:
            self.date = date
        else:
            log.error('Guessing the date from input file is not implemented yet.')
            raise NotImplementedError
        self.headcount = self.extract_headcount()

    @classmethod
    def from_sharepoint(cls, url: str, username: str, password: str, date: str = None):
        """Alternative constructor for files located in SharePoint folders"""
        raise NotImplementedError

    def extract_headcount(self):
        """Extracts complete headcount in prison units from XSLX sheet"""
        log.info(f'Extracting data from {self.original_file}')
        headcount = pd.read_excel(
            self.original_file,
            sheet_name="Efetivo Completo",
            header=None,
            names=[
                'unidadeId',  # A
                'unidadeNome',  # B
                'unidadeLocalidade',  # C
                'efetivoRegime',  # D-E (merged)
                'capacidadeOriginal',  # F
                'capacidadeInospito',  # G
                'capacidadeAtual',  # H
                'efetivoNominal',  # I
                'efetivoBaixados',  # J
                'efetivoAcautelado',  # K
                'efetivoReal',  # L
                'excesso',  # M
                'vagas',  # N
            ],
            usecols='A:D,F:N',
            skiprows=9,
        )
        log.info('Data extracted successfully!')
        return headcount

    def to_csv(self, output_file):
        self.headcount.to_csv(output_file)
