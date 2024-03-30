## Stori Assessment

Name: Julio Jaramillo

#### Introduction

This assessment resolves the problem related to process an CSV file that contains multiples transactions records. It adds support to run in a CLI mode or using an HTTP server. The results are send in an email and stored in database (configuration documentation is described below).

### How can I install it in local?
To run the solution follow the next in a terminal/cli application:
```bash
python@3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cp transactions.csv.example .transactions.csv
```

The next step is configure the ``.env`` values. We will describe each one as follows:

```bash
#####
# Used as email sender address when a account summary report is created
#####
MAIL_USER=theremsoe@gmail.com

#####
# Google mail password required to send emails. You can create one of them
# in the next link: https://myaccount.google.com/apppasswords
#####
MAIL_PASSWORD="bla bla bla bla"

### Database configuration
DB_DATABASE=stori_db
DB_HOST=localhost
DB_USERNAME=postgres
DB_PASSWORD=postgres
``````

Now, you have all minimal elements to run the application.

### Run in CLI mode

To run and test the application logic you can execute the next command in terminal:

```bash
python -m app.cli.account_summary --file '{csv-file-path} --email "{destination@domain.com}"
```

Where ``{csv-file-path}`` is the route to CSV file to process and ``{destination@domain.com}`` is the destination email address to send the final report (account summary information). Substitute those values in your terminal and execute the command. If you wants more details or help about the command you would run the following instruction:

```bash
python -m app.cli.account_summary --help
```

### Run in Http mode

You should run the following command in terminal:
```bash
uvicorn main:app
```

It will create an http server that listen incoming requests. To send a CSV file you can run the next cURL command:

```bash
curl -v 'POST' \
  'http://127.0.0.1:8000/api/v1/account/summary' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@{csv-file-path};type=text/csv' \
  -F 'email={destination@domain.com}'
```

As we described previously, you only need substitute ``{csv-file-path}`` and ``{destination@domain.com}`` variables with you own information. When the request is processed, the server should return a similar output:

```bash
* We are completely uploaded and fine
< HTTP/1.1 200 OK
< date: Sun, 08 Oct 2023 07:46:08 GMT
< server: uvicorn
< content-length: 70
< content-type: application/json
<
* Connection #1 to host 127.0.0.1 left intact
{"status":200,"title":"Ok","detail":"File was processed successfully"}%
```

### Run in Docker mode

It's the most easy way to run the solution. You just need execute the next command in your terminal:

```bash
docker-compose --env-file .env --project-name="stori-assessment" -f .infra/docker-composer.yml up --detach --build
```

And it's all. To test the application you can repeat the cURL command described previously.

#### How it was created?
The core of the solution lives in ``app/business_transactions`` path. Inside it, you can see two files: the first one (``account.py``) contains the core logic to process and get all account summary information that comings from multiple entries like CSV or a DictReader entity. The second one (``entities.py``) contains the models and schemas used to provide an human readable interface. Those models and schemas were created using **Pydantic** to ensure data integrity.

Now, I did create two interfaces to execute the logic: an http endpoint that is described previously and a CLI module. Those interfaces use the same logic contained into ``app/business_transactions/account.py`` file to process csv files. The idea was create a logic that follows the *lego* theorem with the goal of re use the logic in multiple places.

I'm a guy that wants create a robust code. So then, the core logic was created using TDD practice and you can check the tests used to validate the correct functionality in ``tests`` directory.

If you wants check and run the test, please install the required modules contained in ``requirements-dev.txt`` file using ``pip``. Use the next command in a virtual environment active session as guide:

```bash
pip install -r requirements-dev.txt
python -m pytest
```
