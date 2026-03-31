setup-db:
	./database/scripts/create_and_run_database.sh
	./database/sql/00_init_database.py
	./database/sql/01_constraints.py
	./database/sql/02_indexes.py
	./database/seed_database.py

connect-db:
	./databse/scripts/connect_to_database.sh

run:


test:
	tox
