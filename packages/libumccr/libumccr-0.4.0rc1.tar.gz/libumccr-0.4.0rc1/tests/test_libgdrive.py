import csv
import io
import logging
from unittest import TestCase, skip

from libumccr import libgdrive

from libumccr.aws import libssm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LibGDriveUnitTests(TestCase):
    # TODO https://github.com/umccr/libumccr/issues/5
    pass


class LibGDriveIntegrationTests(TestCase):
    # integration test hit actual File or API endpoint, thus, manual run in most cases
    # required appropriate access mechanism setup such as active aws login session
    # uncomment @skip and hit the each test case!
    # and keep decorated @skip after tested

    @skip
    def test_download_sheet1_csv(self):
        """
        python -m unittest tests.test_libgdrive.LibGDriveIntegrationTests.test_download_sheet1_csv
        """
        SHEET_ID = "/umccr/google/drive/lims_sheet_id"
        GDRIVE_SERVICE_ACCOUNT = "/umccr/google/drive/lims_service_account_json"
        lims_sheet_id = libssm.get_secret(SHEET_ID)
        account_info = libssm.get_secret(GDRIVE_SERVICE_ACCOUNT)

        bytes_data = libgdrive.download_sheet1_csv(account_info, lims_sheet_id)
        self.assertIsInstance(bytes_data, bytes)

        # try parse and print last few rows
        csv_reader = csv.DictReader(io.TextIOWrapper(io.BytesIO(bytes_data)))
        for row_number, row in enumerate(csv_reader):
            if row_number > 4116:
                print(row_number, row)
