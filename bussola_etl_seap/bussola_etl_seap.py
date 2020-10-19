"""Classes that model SEAP bulletins and methods to get info from them"""
# pylint: disable=redefined-outer-name,singleton-comparison

import datetime
import json
import re
from typing import List, Mapping, Optional, Tuple, Union
import log
import pandas as pd


class SEAPBulletin:
    """Representation of a weekly bulletin from SEAP/RJ"""

    # TODO: colmapping in a separate configuration file
    # map excel column letters from SEAP/RJ bulletin to desired column names
    colmapping = {
        'A': 'unidadeId',
        'B': 'unidadeNome',
        'C': 'unidadeLocalidade',
        'D': 'efetivoRegime',
        # column E is merged to column D
        'F': 'capacidadeOriginal',
        'G': 'capacidadeInospito',
        'H': 'capacidadeAtual',
        'I': 'efetivoNominal',
        'J': 'efetivoBaixados',
        'K': 'efetivoAcautelado',
        'L': 'efetivoReal',
        'M': 'excesso',
        'N': 'vagas',
    }

    # separate columns by theme
    # TODO: link to colmapping data structure
    id_col = 'unidadeId'
    facility_cols = [
        'unidadeNome',
        'unidadeLocalidade',
        'unidadeTipo',
        'unidadeSigla',
    ]
    capacity_cols = [
        'capacidadeOriginal',
        'capacidadeInospito',
        'capacidadeAtual',
    ]
    imprisoned_cols = [
        'efetivoRegime',
        'efetivoGenero',
        'efetivoNominal',
    ]
    imprisoned_detail_cols = [
        'efetivoBaixados',
        'efetivoAcautelado',
        'efetivoReal',
    ]

    # accepted incarceration types, mapped to their standardized names
    # TODO: map in a separate file
    regime_map = {
        'Aberto': 'Aberto',
        'Fechado': 'Fechado',
        'Med. de Seg.': 'Medidas de Segurança',
        'Provisório': 'Provisório',
        'Semiaberto': 'Semiaberto',
    }

    # value for uncertain or not informed diels
    no_info = "Não Informado"

    custody_count_sheet_name = "Efetivo Completo"
    date_row = 4

    def __init__(
        self,
        input_file: str,
        date: Union[datetime.datetime, str, None] = None
    ) -> None:
        log.info('Initiating bulletin representation...')
        self.input_file = input_file
        _custody_count_sheet = self._read_bulletin(
            sheet_name=self.custody_count_sheet_name,
        )
        # set date of reference
        if date is not None:
            # from user input
            log.info('Setting bulletin date from user input...')
            if isinstance(date, str):
                date = datetime.date.fromisoformat(date)
            self.date = date
        else:
            # from bulletin header
            self.date = self._parse_date(
                bulletin_sheet=_custody_count_sheet,
            )
        log.info(f'Bulletin date set to {self.date.isoformat()}.')
        log.info('Preparing to analyse custody count information...')
        # drop date row and unused column headers
        _custody_count_raw = _custody_count_sheet.loc[8:, :]
        # process count info into a usable format
        _custody_count_parsed = self._parse_count(_custody_count_raw)
        self.facilities = _custody_count_parsed['facilities']
        self.capacity = _custody_count_parsed['capacity']
        self.imprisoned = _custody_count_parsed['imprisoned']
        self.imprisoned_detail = _custody_count_parsed['imprisoned_detail']
        self._summary = None
        # TODO: add summary DataFrame as an attribute

    @classmethod
    def from_sharepoint(
        cls,
        url: str,
        username: str,
        password: str,
        tempdir: Optional[str] = "../data/temp",
        **kwargs,
    ):
        """Get input file from SharePoint before calling the constructor"""
        log.error('Import from SharePoint is not implemented yet!')
        raise NotImplementedError

    def _read_bulletin(
        self,
        sheet_name: str,
    ) -> pd.DataFrame:
        """Extracts raw representation of custody count in XSLX bulletin"""
        log.info(f'Extracting data from {self.input_file}...')
        bulletin_sheet = pd.read_excel(
            io=self.input_file,
            sheet_name=sheet_name,
            header=None,
            names=self.colmapping.values(),
            usecols=','.join(self.colmapping.keys()),
        )
        bulletin_sheet.index.name = 'id'
        log.info('Data extracted successfully!')
        return bulletin_sheet

    def _parse_date(
        self,
        bulletin_sheet: pd.DataFrame,
    ) -> datetime:
        """Get date from raw bulletin data"""
        log.debug('Trying to retrieve date from bulletin header...')
        date_statement = bulletin_sheet.iat[self.date_row, 0]
        log.debug(f"Found date statement: '{date_statement}'. Parsing...")
        date_raw = re.search(
            r'([0-3][0-9]/[0-1][0-9]/20[1-2][0-9])', date_statement
        ).group(0)
        date = datetime.datetime.strptime(date_raw, r'%d/%m/%Y')
        log.info(f"Date automatically set to {date.isoformat()}.")
        return date

    def _parse_count(
        self,
        raw_count: pd.DataFrame
    ) -> Mapping[str, pd.DataFrame]:
        """Parse relevant custody count information from raw bulletin data"""
        log.info('Start parsing raw bulleting data...')
        parsed = raw_count.copy()
        # parse facility types and inmates gender from subtotals
        parsed = self._info_from_subtotals(parsed)
        # fill facility ids in cells that were originally merged in Excel
        log.info('Filling missing IDs...')
        parsed['unidadeSigla'] = ""
        parsed[([self.id_col] + self.facility_cols)] = parsed.loc[
            :, ([self.id_col] + self.facility_cols)].fillna(
            method='ffill',
            axis=0
        )
        # leave only rows with valid ids
        log.info('Deleting rows with subtotals...')
        parsed[self.id_col]= pd.to_numeric(
            parsed[self.id_col],
            errors='coerce'
        )
        parsed = parsed.loc[pd.notna(parsed[self.id_col]), :]
        # complete undefined gender value using patterns in the facility name
        log.info('Getting additional information from facility name field...')
        # remove leading and trailing spaces
        parsed['unidadeNome'] = parsed['unidadeNome'].apply(
            lambda x: x.strip()
        )
        log.debug('    Getting inmates gender...')
        parsed = parsed.apply(
            self._info_from_name,
            axis=1,
            name_patterns={
                'Feminino': r'(?P<unidadeNome>.*)[-– ]FEM[INO]*$',
                'Masculino': r'(?P<unidadeNome>.*)[-– ]MASC[ULINO]*$',
            },
            category_col='efetivoGenero',
            flags=re.IGNORECASE,
        )
        # separate name and abbreviation fields
        log.debug('    Getting facility name abbreviation...')
        parsed = parsed.apply(
            self._info_from_name,
            axis=1,
            name_patterns={
                '_': r'^(?P<unidadeNome>[^-–]*)[-–] *' +
                     r'(?P<unidadeSigla>[A-Z]*)[-– ]*$'
            },
        )
        # remove leading and trailing spaces (again)
        parsed[['unidadeNome', 'unidadeSigla']] = parsed[
            ['unidadeNome', 'unidadeSigla']
        ].applymap(lambda x: x.strip())
        # TODO: complete facility types using patterns in their names (??)
        # standardize regime types
        parsed['efetivoRegime'] = parsed['efetivoRegime'].apply(
            self._parse_regimes
        )
        # make sure facility id column is integer
        parsed[self.id_col] = parsed[self.id_col].astype(int)
        # separate facility data, imprisoned and capacity DataFrames
        log.info('Separating retrieved data...')
        facilities = parsed.loc[:, [self.id_col] + self.facility_cols]
        capacity = parsed.loc[:, [self.id_col] + self.capacity_cols]
        imprisoned = parsed.loc[:, [self.id_col] + self.imprisoned_cols]
        imprisoned_detail = parsed.loc[
            :,
            [self.id_col] + self.imprisoned_detail_cols
        ]
        log.info('Droping empty rows...')
        # discard duplicates from merged cells
        facilities = facilities.dropna().drop_duplicates()
        capacity = capacity.dropna().drop_duplicates()
        imprisoned_detail = imprisoned_detail.dropna().drop_duplicates()
        log.info('Successfully parsed custody count!')
        return {
            'facilities': facilities,
            'capacity': capacity,
            'imprisoned': imprisoned,
            'imprisoned_detail': imprisoned_detail,
        }


    def _info_from_subtotals(
        self,
        count_with_subtotals: pd.DataFrame,
    ) -> pd.DataFrame:
        """Get facility types and inmates gender from bulletin subtotals"""
        log.info('Extracting information custody count subtotals...')
        # get position of main subtotals
        title_fem_id = count_with_subtotals.loc[
            count_with_subtotals[self.id_col] == 'UNIDADES FEMININAS', :
        ].index.values[0]
        title_shelter_id = count_with_subtotals.loc[
            count_with_subtotals[self.id_col] == 'CASA DO ALBERGARDO', :
        ].index.values[0]
        title_hosp_id = count_with_subtotals.loc[
            count_with_subtotals[self.id_col] == 'UNIDADES HOSPITALARES', :
        ].index.values[0]
        # set facility type and gender based on position relative to subtotals
        parsed_count = count_with_subtotals.copy()
        log.info(
            'Setting facility types and inmate genders based on subtotals...'
        )
        # prison-like facilities - set facility type as 'Not Informed'
        parsed_count.loc[:title_shelter_id, 'unidadeTipo'] = self.no_info
        # male prisons
        parsed_count.loc[:title_fem_id, 'efetivoGenero'] = 'Masculino'
        # female prisons
        fem_prison_ids = range(title_fem_id, title_shelter_id)
        parsed_count.loc[fem_prison_ids, 'efetivoGenero'] = 'Feminino'
        # shelters
        shelter_ids = range(title_shelter_id, title_hosp_id)
        parsed_count.loc[shelter_ids, 'unidadeTipo'] = 'Casa do Albergado'
        # hospitals
        parsed_count.loc[
            title_hosp_id:, 'unidadeTipo'
        ] = 'Hospital de Custódia e Tratamento Psiquiatrico'
        # shelters and hospitals don't inform the custody count by gender
        parsed_count.loc[:, 'efetivoGenero'].fillna(
            self.no_info,
            inplace=True,
        )
        # return modified DataFrame
        log.info('Successfully extracted information from subtotals!')
        return parsed_count

    @staticmethod
    def _info_from_name(
        row: pd.Series,
        name_patterns: Mapping[str, str],
        category_col: Optional[str] = None,
        **kwargs,
    ) -> Union[pd.Series, Tuple[str], str]:
        """Get info based on text patterns in facility name field"""
        # if none of the patterns match, return target original values
        log.debug(f"Extracting information for '{row['unidadeNome']}'...")
        for category, pattern in name_patterns.items():
            log.debug(f"Searching regex '{pattern}' in '{row['unidadeNome']}'")
            # check given pattern
            match = re.search(pattern, row['unidadeNome'], **kwargs)
            if match:
                log.debug('    MATCHED!')
                # set column with matched category (if provided)
                if category_col is not None:
                    log.debug(f'    {category_col} set to {category}')
                    row[category_col] = category
                # map captured groups to columns with the same name
                for col, value in match.groupdict().items():
                    row[col] = value
                # if pattern matches, stop searching
                break
        return row

    def _parse_regimes(self, regime_raw: str):
        """Map original regime types to standartized values"""
        try:
            regime = self.regime_map[regime_raw]
        except:
            regime = self.no_info
        finally:
            return regime

    def to_file(
        self,
        output_file: str,
        # TODO: deal with user-specified formats
        tables: Union[str, List[str]] = 'all',
        date_col: Optional[str] = None,
        mode: str = 'w',
        orient: str = 'records',
        # TODO: write mode (append, overwrite, fail)
        **kwargs,
    ) -> None:
        """Export bulletin tables as a local CSV or JSON file"""
        log.info('Preparing to export...')
        # list all subjects user wants to export
        exports = dict()
        if (tables != 'all') & isinstance(tables, str):
            tables = [tables]  # make sure table string is wrapped in a list
        if (tables == 'all') | ('facilities' in tables):
            exports.update({'facilities': self.facilities})
        if (tables == 'all') | ('capacity' in tables):
            exports.update({'capacity': self.capacity})
        if (tables == 'all') | ('imprisoned' in tables):
            exports.update({'imprisoned': self.imprisoned})
        if (tables == 'all') | ('imprisoned_detail' in tables):
            exports.update({'imprisoned_detail': self.imprisoned_detail})
        # deal with export path and extension
        log.debug('    Parsing output file name...')
        try:
            output_basepath, output_format = re.match(
                r'^(.*)\.([a-z]+)$',
                output_file,
                flags=re.IGNORECASE,
            ).group(1, 2)
        except ValueError:
            output_basepath = output_file
            output_format = 'csv'  # TODO: use user-specified format, if given
        # replace [YYYY], [MM] and [DD] in output file name by bulletin date
        output_basepath = re.sub(
            r'\[YYYY\]',
            str(self.date.year),
            output_basepath
        )
        output_basepath = re.sub(
            r'\[MM\]',
            str(self.date.month).zfill(2),
            output_basepath
        )
        output_basepath = re.sub(
            r'\[DD\]',
            str(self.date.day).zfill(2),
            output_basepath
        )
        # TODO: check and deal with appending and overwriting existing files
        # export CSV
        log.debug('    Starting export...')
        for tablename, dataframe in exports.items():
            # TODO: check if file exists and warn/fail
            log.info(f'    Exporting {tablename} table...')
            # add date column, if given
            if date_col is not None:
                log.debug('    Adding date column...')
                dataframe[date_col] = self.date.date()
            # export
            outfile_path = (
                output_basepath + '_' + tablename + '.' + output_format
            )
            with open(outfile_path, mode, encoding='utf-8') as outfile:
                if output_format == 'csv':
                    # replace temporary index
                    dataframe.set_index(self.id_col, inplace=True)
                    # export csv
                    dataframe.to_csv(outfile, mode=mode, **kwargs)
                elif output_format == 'json':
                    # export json
                    dataframe.to_json(
                        outfile,
                        orient=orient,
                        indent=4,
                        force_ascii=False,
                        **kwargs
                    )
                else:
                    log.error(
                        f"Can not export to '{output_format.upper()}' format."
                    )
                    raise RuntimeError
            log.debug(f'    Exported {tablename} table successfully!')
        log.info('Successfully exported files!')
