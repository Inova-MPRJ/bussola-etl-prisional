"""Command Line Interface to extract, transform and load data from SEAP/RJ"""


import datetime
import click
import log
import os 

from typing import Optional, Tuple
from . import bussola_etl_seap


# TODO: chain subcommands for extract, transform and load


@click.command()
@click.option(  # TODO: allow multiple inputs
    '-i',
    '--input-file',
    required=True,
    help='File path, if local; or URL, if remote',
)
@click.option(
    '--date',
    type=click.DateTime(formats=(r'%Y-%m-%d', r'%d-%m-%Y', r'%d/%m/%Y')),
    help='Reference date of the bulletin. ' +
         'If not provided, is guessed from file',
)
@click.option(
    '-e',
    '--export-table',
    default='all',
    show_default=True,
    help='Table to export. Accepted values are "facilities", "capacity", ' +
    '"imprisoned", "imprisoned_details", "occupation" and "all".',
)
@click.option(  # TODO: accept destination folders; combine w/ --to-anvil-table
    '-o',
    '--output-file',
    type=click.Path(writable=True, dir_okay=False, resolve_path=True),
    help='Path and name of the output file.'
)
@click.option(
    '--date-column',
    default=None,
    type=str,
    help='Name of the column with bulletin date, in the exported file.'
    + ''
)
@click.option(  # TODO: accept multiple
    '--to-anvil-table',
    help='Name of an Anvil Data Table to receive the extracted data.\n' + 
    'If not provided and --anvil-token is manually set; or if an empty ' +
    'string ("") is passed, uses the default name for the exported table.',
)
@click.option(
    '--anvil-token',
    type=str,
    help='Anvil Uplink token for Data Table to receive the extracted data. ' +
    'By default, uses the environment variable $ANVIL_TOKEN .',
)
@click.option(  # TODO: other policies
    '-a',
    '--append',
    default=False,
    is_flag=True,
    help='If output file already exists, should append newlines to it? '
    + 'If not and file exists, raises an error.',
)
@click.option(
    '--verbosity',
    default=1,
    type=click.IntRange(min=0, max=3),
    show_default=True,
    help='Set verbosity level of the output. Possible values are: '
    + '0 (Errors), 1 (Warnings), 2 (Info) and 3 (Debug).',
)
def etl(
    input_file: str,
    date: datetime,
    export_table: Tuple[str],
    output_file: Optional[str],
    date_column: Optional[str],
    to_anvil_table: str,
    anvil_token: str,
    append: bool,
    verbosity: int,
) -> None:
    """Get info from a SEAP/RJ bulletin saved as a local .XLSX file"""

    log.reset()
    log.init(verbosity=verbosity)
    # TODO: deal with files in SharePoint
    # TODO: deal with files in e-mail
    # TODO: deal with multiple input files or files in directory
    bulletin = bussola_etl_seap.SEAPBulletin(
        input_file=input_file,
        date=date,
    )
    # process 'all' is present
    if export_table == 'all':
        export_table = bulletin.tables.keys()
    else:
        # TODO: replace with real handler for multiple files
        export_table = [export_table]
    # export to local files
    # TODO: refactor to accept a directory path and export all inside it
    if output_file is not None:
        for table in export_table:
            bulletin.to_file(
                output_file=output_file,
                tablename=table,
                date_col=date_column,
            )
    # export to Anvil
    if (to_anvil_table is not None) or (anvil_token is not None):
        for table in export_table:
            bulletin.to_anvil(
                tablename=table,
                output_table=to_anvil_table,
                token=anvil_token,
                date_col=date_column,
            )

if __name__ == '__main__':  # pragma: no cover
    etl()
