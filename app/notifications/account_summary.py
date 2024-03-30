from locale import currency, setlocale, LC_ALL
from mdmail import send

from app.business_transactions.account import AccountSummary
from config.email import EmailConfig


def account_summary_notification(account_summary: AccountSummary, email: str) -> None:
    """
    Send a notification (email) that contains the account summary information
    """

    setlocale(LC_ALL, "en_US.UTF-8")

    monthly_counters = "\n".join(
        f" - Number of transactions in **{txn.date.strftime('%B')}**: **{txn.count}**"
        for txn in account_summary.transactions
    )

    markdown = f"""
# Stori Software Assessment

### Transaction account summary

 - Total Balance: **{currency(account_summary.balance)}**
{monthly_counters}
 - Average debit amount: **{currency(account_summary.debt_avg)}**
 - Average debit amount: **{currency(account_summary.credit_avg)}**

<img alt="Stori" loading="lazy" width="155.04" height="47.86" decoding="async" style="color:transparent" src="./stori.png">

"""

    send(
        markdown,
        subject="Stori assessment (Julio)",
        from_email="theremsoe@gmail.com",
        to_email=email,
        smtp=EmailConfig().model_dump(),
    )
