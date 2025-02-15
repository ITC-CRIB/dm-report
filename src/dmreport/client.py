import requests
import csv
from enum import Enum
from io import StringIO
import urllib
import datetime
from bs4 import BeautifulSoup
from functools import cache

import logging
logger = logging.getLogger(__name__)


class Report(Enum):
    ASSETS = 21
    TELEMETRY = 43


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


    def get_data(self, id: str, params: dict = None) -> list[dict]:
        result = self.session.post(
            Client.base_url + '/Report/Download',
            data = {
                'ReportId': id,
                'ReportViewId': '0',
                'parameters': urllib.parse.urlencode(
                    {**(params if params else {}), **{'ReportFormat': 'CSV'}}
                ),
                'reportFormatId': '3'
            }
        )
        result.raise_for_status()

        rows = Client.load_csv(result.content.decode('utf-8-sig'));
        return rows


    @cache
    def get_asset_ids(self) -> dict:
        result = self.session.get(
            Client.base_url + '/Report?ReportId=' + str(Report.TELEMETRY.value)
        )
        result.raise_for_status()

        soup = BeautifulSoup(result.text, 'html.parser')

        select = soup.find('select', id = 'AssetId')
        if not select:
            raise ValueError("Invalid response.")

        out = {}
        for option in select.find_all('option'):
            out[option.text] = option.get('value')

        return out;


    def get_asset_id(self, asset) -> str:
        id = self.get_asset_ids().get(asset)
        if not id:
            raise ValueError("Invalid asset code.")
        return id


    def get_assets(self) -> list[dict]:
        return self.get_data(Report.ASSETS.value)


    def get_telemetry(self, asset_id: str, date: datetime.datetime = None) -> list[dict]:
        if not date:
            date = datetime.datetime.now()

        params = {
            'DateUtc': date.strftime('%d/%m/%Y'),
            'AssetId': asset_id,
        }

        return self.get_data(Report.TELEMETRY.value, params)