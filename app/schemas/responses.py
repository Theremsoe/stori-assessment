from pydantic import BaseModel


class AccountSummaryResponse(BaseModel):
    """
    Response model for account summary endpoint
    """
    status: int
    title: str
    detail: str
