from decimal import Decimal
from unittest import TestCase

from app.business_transactions.account import account_summary


class AccountSummaryTest(TestCase):
    def test_balance_and_count(self):
        summary = account_summary(
            [
                {"Id": "0", "Date": "7/15", "Transaction": "+60.5"},
                {"Id": "1", "Date": "7/28", "Transaction": "-10.3"},
                {"Id": "2", "Date": "8/2", "Transaction": "-20.46"},
                {"Id": "3", "Date": "8/3", "Transaction": "+10"},
            ]
        )

        assert summary.count == 4
        assert summary.balance == Decimal("39.74")

    def test_txn_grouping(self):
        summary = account_summary(
            [
                {"Id": "0", "Date": "7/15", "Transaction": "+60.5"},
                {"Id": "1", "Date": "7/28", "Transaction": "-10.3"},
                {"Id": "2", "Date": "8/2", "Transaction": "-20.46"},
                {"Id": "3", "Date": "8/3", "Transaction": "+10"},
            ]
        )

        assert len(summary.transactions) == 2
        assert summary.transactions[0].count == 2
        assert summary.transactions[0].date.isoformat() == "2024-07-01"
        assert summary.transactions[1].count == 2
        assert summary.transactions[1].date.isoformat() == "2024-08-01"

    def test_debt_info(self):
        summary = account_summary(
            [
                {"Id": "0", "Date": "7/15", "Transaction": "+60.5"},
                {"Id": "1", "Date": "7/28", "Transaction": "-10.3"},
                {"Id": "2", "Date": "8/2", "Transaction": "-20.46"},
                {"Id": "3", "Date": "8/3", "Transaction": "+10"},
            ]
        )

        assert summary.debt_count == 2
        assert summary.debt_avg == Decimal("-15.38")

    def test_credit_info(self):
        summary = account_summary(
            [
                {"Id": "0", "Date": "7/15", "Transaction": "+60.5"},
                {"Id": "1", "Date": "7/28", "Transaction": "-10.3"},
                {"Id": "2", "Date": "8/2", "Transaction": "-20.46"},
                {"Id": "3", "Date": "8/3", "Transaction": "+10"},
            ]
        )

        assert summary.credit_count == 2
        assert summary.credit_avg == Decimal("35.25")

    def test_floating_point(self):
        summary = account_summary(
            [
                {"Id": "0", "Date": "7/15", "Transaction": "+0.1"},
                {"Id": "1", "Date": "7/28", "Transaction": "+0.1"},
                {"Id": "2", "Date": "8/2", "Transaction": "+0.1"},
            ]
        )

        assert summary.balance == Decimal("0.3")

    def test_zero_values(self):
        summary = account_summary(
            [
                {"Id": "0", "Date": "7/15", "Transaction": "+0.0"},
            ]
        )

        assert summary.balance == Decimal("0.0")
        assert summary.count == 1
        assert summary.credit_avg == Decimal("0.0")
