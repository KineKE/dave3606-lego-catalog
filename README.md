# DAVE3606 — Resource-efficient Programs Project — 2026
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
This project is my hand-in for the mandatory project for the course [DAVE3606 Resource-efficient Programs](https://student.oslomet.no/en/studier/-/studieinfo/emne/DAVE3606/2025/HØST).
The original course repository from the lecturer, [Åsmund Eldhuset](https://github.com/aasmundeldhuset), can be found [here](https://github.com/aasmundeldhuset/dave3606-project-2026).
The code from the original repository

The original assignment text can also be found under /docs/original_assignment.md, and the original code repository is located in a branch called "starting-point" in this repository.
This preserved and early version of the code is kept intentionally to show the development process and architectural evolution of the codebase.

## Technology


## How to run

> [!TIP]
> To get a full list of `make` commands, use `make help`

### Initial setup

#### 1) Clone this repository

```text
git clone <repo-url>
cd <repo-name>
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

#### 4) Create and seed the database

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

#### 5) Set up enviroment variables

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

### How to use

#### 1) Start Docker container for the database

```text
make start-db
```

<details>
    <summary>Start the database container manually without using make? </summary>

```text
./database/scripts/start_container.sh
```
</details>

#### 2) To connect to the database

```text
make connect-db
````

<details>
    <summary>Connect to the database manually without using make? </summary>

```text
./databse/scripts/connect_to_database.sh
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

## Design decisions


1) Adding a factory pattern to the Flask project.

A factory pattern.... blabla.

Implementing this by making run.py the main entrypoint for running the app by running the app = create_app() function.
In this case, app refers to the folder for the source code for the app itself. 

It consists of, among other things, an __init__.py file. This file create the function for create_app().
It is, in other words, this file that does the actual app creation itself. An app constructor, if you will, which fits its file name.
In the app creation file, the Blueprint is added. 

The file called routes.py is the route handler, as the name suggests.
In the original file, the app was created here, and the routes were attached to this app using @app.routes.
Then the app was created if the file was run as a file (__main__), not as a module. So running this file, was how the server was created.
This creates a high coupling and makes it harder to test.


2) Removing the repeated DB_CONFIG files with the connected psycopg.connect(). This code was repeated a lot, exposes secrets, and would be hard to maintain if anything were to change.






- Lower coupling
- Easier to test
- Greater separation of concern
- Easier to scale


### Overview of the current file structure

#### Directories

- app
-> this is where all of the running code lives

- db_setup
-> this is where the initialization and setup of the database is

- docs
-> this is where documentation for the project is located

- tests
-> the test files for the project lives here


#### Files

##### app directory

- static folder
- templates folder
- __init__.py
- database_connection.py
- kine.py
- queries.py
- routes.py

##### db_setup directory

- scripts directory
- sql directory
- db_seed_bricklink.json.gz
- migrate_database.py
- seed_database.py

##### docs directory


##### tests directory


##### misc in root

- .env
-> the environments for the project

- .env.example
-> a general template for how .env looks, that can be committed to git, so that others can insert their own info, such as passwords and usernames

- Makefile

- README.md

- requirements.txt

- run.py

- tox.ini



Any changes to the database environment, such as the container name, host name, port etc. Make the changes in the .env-file.
You do not need to make changes elsewhere.
This is the one source of truth for environment loading, and it is not hardcoded anywhere else.