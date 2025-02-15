import click

import os
import dotenv
import csv
import json
from enum import Enum
from io import StringIO
import tabulate
import datetime

from .client import Client, Report


import logging
logger = logging.getLogger(__name__)


class OutputFormat(Enum):
    """Output format."""
    CSV = 'csv'
    JSON = 'json'
    TEXT = 'text'
    MARKDOWN = 'markdown'


def get_output(data, format: OutputFormat) -> str:
    if format == OutputFormat.CSV:
        with StringIO() as stream:
            writer = csv.DictWriter(stream, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            out = stream.getvalue()

    elif format == OutputFormat.JSON:
        out = json.dumps(data, indent = 4)

    elif format == OutputFormat.MARKDOWN:
        out = tabulate.tabulate(data, headers = "keys", tablefmt = "github")

    elif format == OutputFormat.TEXT:
        out = tabulate.tabulate(data, headers = "keys")

    else:
        raise ValueError("Invalid output format.")

    return out


@click.command(
    context_settings = {
        'show_default': True,
    },
    help = "Retrieves tracker reports."
)
@click.argument(
    'report',
    type = click.Choice(
        [item.name.lower() for item in Report],
        case_sensitive = False
    )
)
# Configuration options
@click.option(
    '-u',
    '--username',
    type = click.STRING,
    required = True,
    prompt = True,
    help = "Account user name."
)
@click.option(
    '-p',
    '--password',
    type = click.STRING,
    required = True,
    prompt = True,
    hide_input = True,
    help = "Account password."
)
@click.option(
    '-g',
    '--organisation',
    'organisation_id',
    type = click.STRING,
    help = "Organisation id."
)
# Report options
@click.option(
    '--asset',
    type = click.STRING,
    help = "Asset code.",
)
@click.option(
    '--date',
    type = click.DateTime(['%Y-%m-%d']),
    help = 'Telemetry date.',
    default = datetime.datetime.now().strftime('%Y-%m-%d')
)
@click.option(
    '--days',
    type = click.IntRange(min = 1),
    help = 'Number of days.',
    default = 1
)
# Output options
@click.option(
    '-o',
    '--output',
    type = click.Path(),
    help = "Path to store the output."
)
@click.option(
    '-f',
    '--format',
    type = click.Choice(
        [item.value for item in OutputFormat],
        case_sensitive = False
    ),
    default = OutputFormat.TEXT.value,
    help = "Output format."
)
# Development options
@click.option(
    '-d',
    '--debug',
    type = click.BOOL,
    is_flag = True,
    default = False,
    help = "Enable debug mode."
)
# Help options
@click.version_option(
    None,
    '-v',
    '--version',
)
@click.help_option(
    '-h',
    '--help'
)
def cli(
    report,
    username,
    password,
    organisation_id,
    asset,
    date,
    days,
    output,
    format,
    debug
):
    # Set logging level if debug flag is set
    if debug:
        logging.basicConfig(level = logging.DEBUG)
        logger.debug("Debugging enabled.")

    # Create client
    client = Client(
        username = username,
        password = password,
        organisation_id = organisation_id,
    )

    # Get report data
    report = Report[report.upper()]

    if report == Report.ASSETS:
        data = client.get_assets()

    elif report == Report.TELEMETRY:
        if not asset:
            click.echo("No asset code.")
            exit(1)

        asset_id = client.get_asset_id(asset)

        data = []
        for day in range(1, days + 1):
            data.extend(client.get_telemetry(asset_id, date))
            date += datetime.timedelta(days = 1)

    else:
        raise ValueError("Invalid report type.")

    # Generate output
    out = get_output(data, OutputFormat(format))

    # Check if output to a file is requested
    if output:
        # Store output
        with open(output, 'w', encoding='utf-8') as file:
            file.write(out)

    else:
        # Display output
        click.echo(out)


def main():
    dotenv.load_dotenv(os.path.join(os.getcwd(), '.env'))
    cli(auto_envvar_prefix = 'DM')
