"""Command Line Interface to extract, transform and load data from SEAP/RJ"""


import datetime
import click
import log

from bussola_etl_seap import SEAPBulletin


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
    '-o',
    '--output-file',
    default='./data/output/[YYYY][MM][DD]_SEAPRJ.csv',
    type=click.Path(writable=True, dir_okay=False, resolve_path=True),
    help='Path and name of the output file. '
    + 'If not specified, it is saved in the package /data/output folder,'
    + "preceded by the bulletin's reference date and succedded by "
    + 'the subject. Ex. 20200811_SEAPRJ_facilities.csv',
)
@click.option(
    '--date-column',
    default=None,
    type=str,
    help='Name of the column with bulletin date, in the exported file.'
    + ''
)
@click.option(
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
    output_file: str,
    date_column: str,
    append: bool,
    verbosity: int,
) -> None:
    """Get info from a SEAP/RJ bulletin saved as a local .XLSX file"""

    log.reset()
    log.init(verbosity=verbosity)
    # TODO: deal with files in SharePoint
    # TODO: deal with files in e-mail
    # TODO: deal with multiple input files or files in directory
    bulletin = SEAPBulletin(
        input_file=input_file,
        date=date,
    )
    if output_file is not None:
        bulletin.to_file(
            output_file,
            tables='all',  # TODO: accept other outputs
        )


if __name__ == '__main__':  # pragma: no cove
    etl()
