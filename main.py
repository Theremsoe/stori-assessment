from decimal import Decimal
from tempfile import NamedTemporaryFile
from typing import Annotated
from fastapi import BackgroundTasks, FastAPI, Form, UploadFile

from app.models.file import File
from app.models.transaction import Transaction
from app.models.database import SessionLocal, Base, engine
from app.business_transactions.account import account_summary_from_file
from app.notifications.account_summary import account_summary_notification
from app.schemas.responses import AccountSummaryResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

def async_account_summary(file: UploadFile, email: str):
    with NamedTemporaryFile() as stream:
        stream.write(file.file.read())

        stream.seek(0)

        summary = account_summary_from_file(stream.name)
        account_summary_notification(summary, email)

    with SessionLocal.begin() as session:
        file_db = File(
            name=file.filename,
            transactions=[
                Transaction(date=txn.get('Date'), transaction=Decimal(txn.get('Transaction')))
                    for txn in summary.records
            ])
        session.add(file_db)


@app.post("/api/v1/account/summary", status_code=200)
def account_summary(
    file: UploadFile,
    email: Annotated[str, Form()],
    background_tasks: BackgroundTasks
) -> AccountSummaryResponse:
    """
    Retrieve a file and process it in a asynchronous task
    """

    background_tasks.add_task(async_account_summary, file, email)

    return AccountSummaryResponse(
        status=200, title="Ok", detail="File was processed successfully"
    )
