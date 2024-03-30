from csv import DictReader
from datetime import date
from decimal import Decimal
from typing import List, Optional

from app.business_transactions.entities import (
    AccountSummary,
    Transaction,
    TransactionRaw,
)


# IO[str]
def account_summary(reader: DictReader | List[TransactionRaw]) -> AccountSummary:
    """
    Given a dictionary reader, generates account summary information
    """
    summary = AccountSummary()
    timestamp: date = date.today()
    row_txn: TransactionRaw

    for row_txn in reader:
        amount = Decimal(row_txn.get("Transaction"))

        summary.records.append(row_txn)
        summary.balance += amount
        summary.count += 1

        if amount < Decimal("0.00"):
            summary.debt_count += 1
            summary.debt_avg += amount
        else:
            summary.credit_count += 1
            summary.credit_avg += amount

        month, _ = row_txn.get("Date", "").split("/")
        txn_date = timestamp.replace(day=1, month=int(month))

        txn: Optional[Transaction] = next(
            (txn for txn in summary.transactions if txn_date == txn.date), None
        )

        if txn is None:
            txn = Transaction(date=txn_date)
            summary.transactions.append(txn)

        txn.count += 1

    if summary.debt_count:
        summary.debt_avg /= Decimal(summary.debt_count)

    if summary.credit_count:
        summary.credit_avg /= Decimal(summary.credit_count)

    return summary
