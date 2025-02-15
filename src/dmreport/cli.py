from .client import Client, Report

import click

import logging
logger = logging.getLogger(__name__)


@click.command(
    context_settings = {
        'show_default': True,
    },
    help = "Retrieves tracker reports."
)
@click.argument(
    'report',
)
# Configuration options
@click.option(
    '-e',
    '--env',
    type = click.File('r', encoding = 'utf-8'),
    default = '.env',
    help = "Path of the environment file."
)
@click.option(
    '-u',
    '--username',
    type = click.STRING,
    prompt = True,
    envvar = 'DM_USERNAME',
    help = "Account user name."
)
@click.option(
    '-p',
    '--pasword',
    type = click.STRING,
    prompt = True,
    envvar = 'DM_PASSWORD',
    hide_input = True,
    help = "Account password."
)
@click.option(
    '-g'
    '--organisation-id',
    type = click.STRING,
    envvar = 'DM_ORGANISATION_ID',
    help = "Organisation id."
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
    )
    default = OutputFormat.MARKDOWN.value,
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
def main(
    report,
    env,
    username,
    password,
    output,
    format,
    debug
):
    # Set logging level if debug flag is set
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug("Debugging enabled.")

    # Create client
    client = Client(
        username = username,
        password = password,
        organisation_id = organisation_id,
    )

    # Get report result
    result = client.get_report(Report(report))

    # Generate output
    out = get_output(result, OutputFormat(format))

    # Check if output to a file is requested
    if output:
        # Store output
        with open(output, 'w', encoding='utf-8') as file:
            file.write(out)

    else:
        # Display output
        click.echo(out)
