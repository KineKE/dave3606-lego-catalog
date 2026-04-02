# DAVE3606 — Resource-Efficient Programs Project — 2026
> LEGO catalog database

![LEGO banner](https://firstbook.org/wp-content/uploads/2022/08/lego-landing-page-hero.png)


## To Åsmund, Alexander and Nathaniel

| Task # |            Location            | Explanation                                                                      |
|:------:|:------------------------------:|----------------------------------------------------------------------------------|
| Report |         docs/report.md         | Describes design choices, SQL statements and performance reasoning               |
| Task 1 | database/sql/01_constraints.py | Adds PK and FK constraints to the existing schema                                |
| Task 2 |   database/sql/02_indexes.py   | Adds indexes to support brick-type and color-based searches combined with set id |
| Task 3 |                                |                                                                                  |
| Task 4 |                                |                                                                                  |
| Task 5 |                                |                                                                                  |
| Task 6 |                                |                                                                                  |
| Task 7 |                                |                                                                                  |


## About this project


https://github.com/aasmundeldhuset/dave3606-project-2026

The original assignment can also be found under /docs/original_assignment.md

## Stack


## How to run

> [!TIP]
> To get a full list of `make` commands, use `make help`

### Initial setup

#### Clone this repository

```text
git clone <repo-url>
cd <repo-name>
```

#### Create and activate a virtual environment

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

#### Install dependencies

```text
make install
```

<details>
    <summary>Install dependencies manually without using make? </summary>

```text
pip install -r requirements.txt
```
</details>

#### Create and seed the database

```text
make setup-db
```

<details>
    <summary>Initiate and set up the database manually without using make? </summary>


```text
./database/scripts/create_and_run_database.sh
./database/sql/00_init_database.py
./database/sql/01_constraints.py
./database/sql/02_indexes.py
./database/seed_database.py
```
</details>

#### Set up enviroment variables

```text
make env
```
<details>
    <summary>Set up the environment manually without using make? </summary>

```text
cp .env.example .env
```
</details>

Then adjust the values in .env if needed, such as database username and password


### How to use

#### Start Docker container for the database

```text
make start-db
```

<details>
    <summary>Start the database container manually without using make? </summary>

```text
./database/scripts/start_container.sh
```
</details>

#### To connect to the database

```text
make connect-db
````

<details>
    <summary>Connect to the database manually without using make? </summary>

```text
./databse/scripts/connect_to_database.sh
```

</details>

#### To run the app:
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

I have added `tox` to project, which ensures reproducible test execution in a controlled environment. It runs on `pytest`.
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
./database/scripts/stop_container.sh
```
</details>

