from decimal import Decimal
from click import echo, style, command, option, Path

from app.models.database import SessionLocal, Base, engine
from app.models.file import File
from app.models.transaction import Transaction
from app.business_transactions.account import account_summary_from_file
from app.notifications.account_summary import account_summary_notification

Base.metadata.create_all(bind=engine)

@command
@option('--file', help="Path to transactions csv file", required=True, type=Path(exists=True))
@option('--email', help="Destination email address", required=True)
def cli_account_summary(file: str, email: str) -> None:
    """
    CLI account summary

    Reads a CSV file from options and send an email with all account summary information
    """

    summary = account_summary_from_file(file)

    account_summary_notification(summary, email)

    with SessionLocal.begin() as session:
        file_db = File(
            name=file,
            transactions=[
                Transaction(date=txn.get('Date'), transaction=Decimal(txn.get('Transaction')))
                    for txn in summary.records
            ])
        session.add(file_db)

    echo(
        style(
            f"An account summary report was sent to {email}",
            bold=True,
            fg="white",
            bg="green",
        )
    )


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli_account_summary()
