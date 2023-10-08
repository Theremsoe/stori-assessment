from csv import DictWriter
from decimal import Decimal
from tempfile import NamedTemporaryFile
from unittest import TestCase

from app.business_transactions.account import account_summary_from_file


class AccountSummaryFromFileTest(TestCase):
    def test_account_summary(self):
        with NamedTemporaryFile("w+", encoding='utf-8') as stream:
            csv = DictWriter(stream, fieldnames=['Id', 'Date', 'Transaction'])
            csv.writeheader()
            csv.writerows([
                {'Id': '0', 'Date': '7/15', 'Transaction': '+60.5'},
                {'Id': '1', 'Date': '7/28', 'Transaction': '-10.3'},
                {'Id': '2', 'Date': '8/2', 'Transaction': '-20.46'},
                {'Id': '3', 'Date': '8/3', 'Transaction': '+10'},
            ])

            stream.seek(0)

            summary = account_summary_from_file(stream.name)

            assert summary.count == 4
            assert summary.balance == Decimal('39.74')
