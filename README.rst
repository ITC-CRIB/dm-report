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


Usage
-----

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


Instead of passing arguments to the constructor method, client parameters can
be specified using the following environment variables:

- ``DM_USERNAME``: Username.
- ``DM_PASSWORD``: Password.
- ``DM_ORGANISATION_ID``: Organisation id.

If a ``.env`` file exists in the working directory, the package automatically
reads environment variables from the file.


Acknowledgements
----------------

This software was developed as part of the research project `SmartAvocado`_
funded by the `Dutch Research Council (NWO) Open Competition Domain Science
XS 2023 <NWO-XS>`_.

.. _SmartAvocado: https://www.utwente.nl/en/smartavocado/
.. _NWO-XS: https://www.nwo.nl/en/researchprogrammes/
