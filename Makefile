# Install requirements/dependencies for the project
install:


# Database setup and migration
setup-db:
	./database/scripts/create_and_run_database.sh
	./database/sql/00_init_database.py
	./database/sql/01_constraints.py
	./database/sql/02_indexes.py
	./database/seed_database.py

# Start the Docker container with the database
start-db:
	./database/scripts/start_container.sh

# Stop the Docker container with the database
stop-db:
	./database/scripts/stop_container.sh

# Connect to the database (after it has been started)
connect-db:
	./databse/scripts/connect_to_database.sh

# Run the web app
run:
	python ./app/server.py

# Run the full test suite
test:
	tox

help:
	@echo "Available targets: "
	@echo "	make install	- install requirements for the project"
	@echo "	make setup-db	- initialize the database and run migrations"
	@echo "	make start-db	- start the Docker container with the database"
	@echo "	make stop-db	- stop the Docker container with the database"
	@echo "	make connect-db	- connect to the database (after it has been started)"
	@echo "	make run	- run the application"
	@echo "	make test	- run tests and linter with tox"