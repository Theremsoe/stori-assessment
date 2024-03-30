from io import TextIOWrapper
from typing import Annotated
from fastapi import BackgroundTasks, Form, UploadFile, APIRouter

from app.http.resources.account import AccountSummaryResponse
from app.jobs.account_summary_job import account_summary_job

account_summary_router = APIRouter()


@account_summary_router.post("/account/summary", status_code=200)
def account_summary(
    file: UploadFile, email: Annotated[str, Form()], background_tasks: BackgroundTasks
) -> AccountSummaryResponse:
    background_tasks.add_task(
        account_summary_job,
        TextIOWrapper(file.file, encoding="utf-8"),
        email,
        file.filename,
    )

    return AccountSummaryResponse(
        status=200, title="Ok", detail="Retrieved file. Process it."
    )
