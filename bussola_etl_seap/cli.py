"""Command Line Interface to extract, transform and load data from SEAP/RJ"""

import click
import log

from bussola_etl_seap import SEAPBulletin


# TO-DO: chain subcommands for extract, transform and load


@click.command()
@click.option(
    '-i',
    '--input-file',
    required=True,
    help='File path, if local; or URL, if remote')
@click.option(
    '--date',
    # TO-DO: define as click.DateTime type
    help='Reference date of the bulletin. ' +
         'If not provided, is guessed from file',
)
@click.option(
    '-o',
    '--output-file',
    default='./data/output/[YYYY]-[MM]-[DD]_SEAP-RJ_Bulletin.csv',
    type=click.Path(writable=True, dir_okay=False, resolve_path=True),
    help='Path and name of the output file. '
    + 'If not specified, it is saved in the package /data/output folder,'
    + "and preceded by the bulletin's reference date. "
    + 'Ex. 2020-08-11_SEAP-RJ_Bulletin.csv',
)
@click.option(
    '-a',
    '--append',
    default=True,
    type=bool,
    show_default=True,
    help='If output file already exists, should append newlines to it?',
)
@click.option(
    '--verbosity',
    default=1,
    type=int,
    show_default=True,
    help='Set verbosity level of the output. Possible values are: '
    + '0 (Errors), 1 (Warnings), 2 (Info) and 3 (Debug).',
)
def etl(
        input_file: str,
        date: str,  # TO-DO: datetime
        output_file: str,
        append: bool,
        verbosity: int,
) -> None:
    """Get info from a SEAP/RJ bulletin saved as a local .XLSX file"""

    log.reset()
    log.init(verbosity=verbosity)
    # TO-DO: deal with remote files
    bulletin = SEAPBulletin(input_file, date=date)
    # TO-DO: everything else
    if output_file is not None:
        bulletin.to_csv(output_file)


if __name__ == '__main__':  # pragma: no cover
    etl()
