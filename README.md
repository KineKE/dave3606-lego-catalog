# DAVE3606 — Resource-efficient Programs Project — 2026
> LEGO catalog

![LEGO banner](https://firstbook.org/wp-content/uploads/2022/08/lego-landing-page-hero.png)


## Where the assignment tasks are implemented

| Task # |                                         Location                                         | Explanation                                                                                                                      |
|:------:|:----------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------|
| Report |                                      docs/report.md                                      | Describes design choices, SQL statements and performance reasoning                                                               |
| Task 1 |                                 db_setup/sql/schema.sql                                  | Adds PK and FK constraints to the existing schema                                                                                |
| Task 2 |                                 db_setup/sql/schema.sql                                  | Adds indexes to support brick-type and color-based searches combined with set id                                                 |
| Task 3 |                           app/routes.py  + app/routes_utils.py                           | Improving algorithmic complexity                                                                                                 |
| Task 4 |                           app/routes.py + app/routes_utils.py                            | Encoding, compression, file handle safety                                                                                         |
| Task 5 |                        app/kine.py + app/kinecat + app/routes.py                         | Creates JSON dump and custom binary file format + implements the logic in the endpoint                                           |
| Task 6 |       app/templates/set.html + app/cache.py + app/routes.py + app/routes_utils.py        | Adds javascript to display the set inventory information + creates cache-file + implements cache-logic in routes and helper file |
| Task 7 | app/database.py + app/database_session.py + app/routes.py + app/routes_utils.py + tests/ | Adds tests, creates DI with Databse wrappers, simplifies endpoint logic                                                          |


## About this project
This project is my hand-in for the mandatory project for the course [DAVE3606 Resource-efficient Programs](https://student.oslomet.no/en/studier/-/studieinfo/emne/DAVE3606/2025/HØST).
The original course repository from the lecturer, [Åsmund Eldhuset](https://github.com/aasmundeldhuset), can be found [here](https://github.com/aasmundeldhuset/dave3606-project-2026).

The original assignment text can also be found under /docs/original_assignment.md, and the original code repository is located in a branch called "starting-point" in this repository.
This preserved and early version of the code is kept intentionally to show the development process and architectural evolution of the codebase.

Starting from the unfinished course repository, I restructured the application, improved the database model, added 
indexing and caching, implemented JSON and binary export, and introduced a cleaner testing setup.

## Repository overview

### Main folders

- `app/` — Flask application code, templates, static files, cache, database helpers, and the custom `.kine` format tools
- `db_setup/` — database schema, seed file, setup scripts, and helper shell scripts
- `docs/` — project documentation and report
- `tests/` — automated tests for database/session logic and endpoints

## Technology used

- **Python**
- **Flask**
- **PostgreSQL**
- **psycopg**
- **Docker**
- **pytest**
- **tox**
- **flake8**


## Design decisions

**Design summary**


Compared with the original course starter code, I made a few larger structural changes:
- Introduced an application factory in app/__init__.py and used run.py as the entrypoint
- Implemented a .env file for a centralized solution for variables
- Replaced repeated database connection code with a dedicated DatabaseSession context manager
- Added a Database helper class to centralize SQL execution
- Moved SQL into queries.py
- Added Makefile commands to simplify setup and execution
- Added tests, tox, and flake8
- Split database setup into a separate db_setup/ area

These changes were mainly made to improve readability, reduce repeated code, and make the project easier to test and maintain.


Any changes to the database environment, such as the container name, host name, port etc. Make the changes in the .env-file.
You do not need to make changes elsewhere.
This is the one source of truth for environment loading, and it is not hardcoded anywhere else.

## How to run

> [!TIP]
> To get a full list of `make` commands, use `make help`

### To run a full setup

Assuming Python 3 and Docker are installed.
Make sure Docker Desktop is up and running.

Then, the full setup can be done by running this:

```text
git clone https://github.com/KineKE/dave3606-lego-catalog.git
cd dave3606-lego-catalog

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
make env
make setup-db
make run
```

### To run the set up step by step. Initial setup.

#### 1) Clone this repository

```text
git clone https://github.com/KineKE/dave3606-lego-catalog.git
cd dave3606-lego-catalog
```

#### 2) Create and activate a virtual environment

```text
python -m venv .venv
source .venv/bin/activate
```
<details>
    <summary>If you unfortunately are on Windows</summary>

```text
.venv\Scripts\activate
```
</details>

#### 3) Install dependencies

```text
make install
```

<details>
    <summary>Install dependencies manually without using make? </summary>

```text
pip install -r requirements.txt
```
</details>

#### 4) Set up environment variables

```text
make env
```
<details>
    <summary>Set up the environment manually without using make? </summary>

```text
cp .env.example .env
```
</details>

Then adjust the values in .env if needed, such as database username and password.
As this is a student project where we have set out own values, there is no need to make changes, it will work with the values provided as defaults.


#### 5) Create and seed the database

```text
make setup-db
```

<details>
    <summary>Initiate and set up the database manually without using make? </summary>


```text
./db_setup/scripts/create_and_run_db.sh
./db_setup/setup_database.py
./db_setup/seed_database.py
```
</details>


### How to use

#### 1) Start Docker container for the database

```text
make start-db
```

<details>
    <summary>Start the database container manually without using make? </summary>

```text
./db_setup/scripts/start_container.sh
```
</details>

#### 2) To connect to the database

```text
make connect-db
````

<details>
    <summary>Connect to the database manually without using make? </summary>

```text
./db_setup/scripts/connect_to_db.sh
```

</details>

#### 3) To run the app:
The recommended way to run the application is:

```text
make run
```
This starts the Flask app through the root-level `run.py` entrypoint.


<details>
    <summary>Run the app manually without using make? </summary>

```text
python run.py
```
</details>

Then, open the local address shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

### Running tests

I have added `tox` to the project, which ensures reproducible test execution in a controlled environment. It uses on `pytest`.
A linter called `flake8` has also been added to tox' test environment and will be run along with the `tox` test suite.

To run the full test suite:
```text
make test
```

<details>
    <summary>Run the tox test suite without using make? </summary>

```text
tox
```
</details>

<details>
    <summary>Run tests manually without using tox? </summary>

```text
pytest
```
</details>

#### Stop Docker container for the database

```text
make stop-db
```
<details>
    <summary>Stop container for the database without using make? </summary>

```text
./db_setup/scripts/stop_container.sh
```
</details>
