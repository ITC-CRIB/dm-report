DM-Report
=========

This is a package and command-line utility to collect data from Digital Matter
trackers.


Installation
------------

1. Clone or download the `source code <https://github.com/ITC-CRIB/dm-report>`_:

   .. code:: shell

      git clone https://github.com/ITC-CRIB/dm-report.git

2. Go to the root directory:

   .. code:: shell

      cd dm-report/

3. Compile and install using pip:

   .. code:: shell

      pip install .


CLI Usage
---------

.. code:: console

   Usage: dmreport [OPTIONS] {assets|telemetry}

     Retrieves tracker reports.

   Options:
     -u, --username TEXT             Account user name.  [required]
     -p, --password TEXT             Account password.  [required]
     -g, --organisation TEXT         Organisation id.
     --asset TEXT                    Asset code.
     --date [%Y-%m-%d]               Telemetry date.  [default: 2025-02-17]
     --days INTEGER RANGE            Number of days.  [default: 1; x>=1]
     -o, --output PATH               Path to store the output.
     -f, --format [csv|json|text|markdown]
                                     Output format.  [default: text]
     -d, --debug                     Enable debug mode.
     -v, --version                   Show the version and exit.
     -h, --help                      Show this message and exit.


Instead of passing arguments to command-line utility, you can also use
the following environment variables:

- ``DM_USERNAME``: Username.
- ``DM_PASSWORD``: Password.
- ``DM_ORGANISATION_ID``: Organisation id.

If a ``.env`` file exists in the working directory, the command-line utility
automatically reads environment variables from the file.


Basic example to retrieve information about the assets as CSV:

.. code:: console

   dmreport assets --format csv --output assets.csv


Basic example to retrieve telemetry information of an asset for a specified
number of days starting from a starting date as CSV:

.. code:: console

   dmreport telemetry --asset my_asset --date 2025-01-02 --days 15 --format csv --output telemetry.csv


Package Usage
-------------

Basic example to retrieve information about the assets:

.. code:: python

   from dmreport.client import Client

   # Create a client
   client = Client('username', 'password', organisation_id = 'organisation_id')

   # Retrieve assets report
   assets = client.get_assets()


Basic example to retrieve telemetry data of an asset for a specific date:

.. code:: python

   from dmreport.client import Client
   from datatime import datetime

   # Create a client
   client = Client('username', 'password', organisation_id = 'organisation_id')

   # Get asset telemetry
   telemetry = client.get_telemetry(
       client.get_asset_id('asset_code'),
       datetime.strptime('yyyy-mm-dd', '%Y-%m-%d')
   )


Acknowledgements
----------------

This software was developed as part of the research project `SmartAvocado`_
funded by the `Dutch Research Council (NWO) Open Competition Domain Science
XS 2023 <NWO-XS>`_.

.. _SmartAvocado: https://www.utwente.nl/en/smartavocado/
.. _NWO-XS: https://www.nwo.nl/en/researchprogrammes/
