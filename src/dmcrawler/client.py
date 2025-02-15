import requests
import csv
from enum import Enum
from io import StringIO


class Report(Enum):
    Assets = 21
    
    
class Client:
    base_url = 'https://lescav.telematics.guru'

    def __init__(self, username: str, password: str, organisation_id: str = None):
        # Start session
        self.session = requests.Session()

        # Login
        self.session.post(
            Client.base_url + '/Account/LogIn',
            data = {
                'UserName': username,
                'Password': password,
            }
        )

        # Select organization if required
        if organisation_id:
            self.session.post(
                Client.base_url + '/Account/SelectOrganisation',
                data = {
                    'OrganisationId': organisation_id,
                }
            )


    def __del__(self):
        # Close session
        self.session.close()


    def load_csv(data: str) -> list:
        rows = []

        with StringIO(data) as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                rows.append(row)

        return rows


    def get_report(id: Report):
        result = self.session.post(
            Client.base_url + '/Report/Download',
            data = {
                "ReportId": id,
                "ReportViewId": "0",
                "parameters": "ReportFormat=CSV&EXCEL.WrapHeaders=false&EXCEL.FreezePanes=false",
                "reportFormatId": "3"
            }
        )
        rows = Client.load_csv(result.content.decode('utf-8-sig'));
        return rows