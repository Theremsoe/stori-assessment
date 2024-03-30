from csv import DictReader
from decimal import Decimal
from typing import Iterable

from app.models.database import SessionLocal
from app.models.file import File
from app.models.transaction import Transaction
from app.business_transactions.account import account_summary
from app.notifications.account_summary import account_summary_notification


def account_summary_job(input: Iterable[str], email: str, filename: str):
    reader = DictReader(input, strict=True)

    summary = account_summary(reader)
    account_summary_notification(summary, email)

    with SessionLocal.begin() as session:
        file_db = File(
            name=filename,
            transactions=[
                Transaction(
                    date=txn.get("Date"), transaction=Decimal(txn.get("Transaction"))
                )
                for txn in summary.records
            ],
        )
        session.add(file_db)
