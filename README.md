# UniLabs API  :test_tube:

This is the API for UniLabs Inventory Management System


## Setup Guide :raised_hands:

### Python Environment Setup 

Make sure you have python 3.6 or newer installed on your computer. If so, clone this repository to your local computer.

```bash
$ git clone https://github.com/UniLabsIMS/UniLabs-API.git
$ cd UniLabs-API
```

Then create a virtual environment to run the project in. The commands may change depending on the operating system you are using. For windows,

```bash
$ python -m venv env
$ .\env\Scripts\activate.bat
```

Then install dependencies needed in the virtual environment

```bash
(venv) pip install -r requirements.txt 
```

Check if following command prints the available commands. If the installation is successful, this should not cause an error.

```bash
(venv) python manage.py
```

### Postgres Setup

Install [PostgreSQL](https://www.postgresql.org/) in the local machine and setup correctly. Use the following command to log in to the `psql` shell as `postgres` user.

```bash
$ psql -U postgres
```
Then create a new database and exit the `psql` shell

```bash
(psql) CREATE DATABASE unilabs_API;
(psql) \q
```
### Django Setup

Contact a team member and setup .env file with sensitive information

First, run the database migration and create the necessary tables. Make sure you are in the correct virtual environment. Whenever there is a database model change, you should re-run this.

```bash
(env) python manage.py makemigrations
(env) python manage.py migrate
```

Afterward, try running the API

```bash
(env) python manage.py runserver
```

## Starting a New Feature :hammer_and_wrench:

Activate the virtual environemnt

```bash
$ .\env\Scripts\activate.bat
```

Checkout main and pull changes

```bash
(env) git checkout main
(env) git pull
```

checkut to a new branch
```bash
(env) git checkout -b feature/<feature_name>
```

install missing dependancies and rerun migrations

```bash
(env) pip install -r requirements.txt
(env) python manage.py makemigrations
(env) python manage.py migrate
```
Start and run API

```bash
(env) python manage.py runserver
```

