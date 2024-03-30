from click import echo, style, command, option, Path

from app.jobs.account_summary_job import account_summary_job
from app.models.database import Base, engine

Base.metadata.create_all(bind=engine)


@command
@option(
    "--file",
    help="Path to transactions csv file",
    required=True,
    type=Path(exists=True),
)
@option("--email", help="Destination email address", required=True)
def cli_account_summary(file: str, email: str) -> None:
    with open(file, "r", encoding="utf-8") as input:
        account_summary_job(input, email, file)

    echo(
        style(
            f"An account summary report was sent to {email}",
            bold=True,
            fg="white",
            bg="green",
        )
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli_account_summary()
