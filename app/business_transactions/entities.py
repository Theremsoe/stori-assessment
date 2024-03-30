from datetime import date
from decimal import Decimal
from typing import List
from typing_extensions import TypedDict

from pydantic import BaseModel


class TransactionRaw(TypedDict):
    """
    Transaction raw
    """

    Id: str
    Date: str
    Transaction: str


class Transaction(BaseModel):
    """
    transaction resume per date
    """

    date: date
    count: int = 0


class AccountSummary(BaseModel):
    """
    Account summary info
    """

    count: int = 0
    """Transactions count"""

    balance: Decimal = Decimal("0.00")
    """Transactions balance"""

    transactions: List[Transaction] = []
    """Monthly summary list"""

    debt_avg: Decimal = Decimal("0.00")
    debt_count: int = 0
    credit_avg: Decimal = Decimal("0.00")
    credit_count: int = 0

    records: List[TransactionRaw] = []
