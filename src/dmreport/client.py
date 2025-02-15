import requests
import csv
from enum import Enum
from io import StringIO


import logging
logger = logging.getLogger(__name__)


class Report(Enum):
    Assets = 21


class Client:
    base_url = 'https://lescav.telematics.guru'

    def __init__(self, username: str, password: str, organisation_id: str = None):
        # Start session
        self.session = requests.Session()

        # Login
        logger.debug(f"Logging in {username}.")
        result = self.session.post(
            Client.base_url + '/Account/LogIn',
            data = {
                'UserName': username,
                'Password': password,
            }
        )
        if result.status_code != 200:
            raise ValueError("Invalid username or password.")

        # Select organization if required
        if organisation_id:
            logger.debug(f"Selecting organisation {organisation_id}.")
            result = self.session.post(
                Client.base_url + '/Account/SelectOrganisation',
                data = {
                    'OrganisationId': organisation_id,
                }
            )
            if result.status_code != 200:
                raise ValueError("Invalid organisation id.")


    def __del__(self):
        # Close session
        self.session.close()


    @staticmethod
    def load_csv(data: str) -> list:
        rows = []

        with StringIO(data) as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                rows.append(row)

        return rows


    def get_report(self, id):
        result = self.session.post(
            Client.base_url + '/Report/Download',
            data = {
                "ReportId": id.value if isinstance(id, Enum) else id,
                "ReportViewId": "0",
                "parameters": "ReportFormat=CSV",
                "reportFormatId": "3"
            }
        )
        result.raise_for_status()

        rows = Client.load_csv(result.content.decode('utf-8-sig'));
        return rows