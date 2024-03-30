from pydantic import BaseModel


class AccountSummaryResponse(BaseModel):
    status: int
    title: str
    detail: str
