PYTHON=./env/bin/python3
DB_NAME=pmaapi
DB_USER=pmaapi
DB_PW=pmaapi
SRC=pmaapi
TEST=test/


.PHONY: lint tags ltags test all lint_all codestyle docstyle server serve lint_src lint_test doctest doc code linters_all code_src code_test doc_src doc_test

# Batched Commands
all: linters_all test_all
lint: lint_src code_src doc_src
linters_all: doc code lint_all

# Pylint Only
lint_all: lint_src lint_test
lint_src:
	${PYTHON} -m pylint --output-format=colorized --reports=n ${SRC}
lint_test:
	${PYTHON} -m pylint --output-format=colorized --reports=n ${TEST}

# PyCodeStyle Only
codestyle: codestyle_src codestyle_test
code_src: codestyle_src
code_test: codestyle_test
code: codestyle
codestyle_src:
	${PYTHON} -m pycodestyle ${SRC}
codestyle_test:
	${PYTHON} -m pycodestyle ${TEST}

# PyDocStyle Only
docstyle: docstyle_src docstyle_test
doc_src: docstyle_src
doc_test: docstyle_test
doc: docstyle
docstyle_src:
	${PYTHON} -m pydocstyle ${SRC}
docstyle_test:
	${PYTHON} -m pydocstyle ${TEST}

# Text Editor Commands
tags:
	ctags -R --python-kinds=-i .
ltags:
	ctags -R --python-kinds=-i ./${SRC}

# Testing
test_all: unittest doctest
unittest: test
test:
	${PYTHON} -m unittest discover -v
doctest:
	${PYTHON} -m test.test_ppp --doctests-only

# Server Commands
serve:server
server:
	gunicorn pmaapi.__main__:APP

# DB Commands
DB_COMMAND=psql postgres -c
ENCODING=UTF8
setup_db: create_db create_users set_privileges export_vars
create_db: # Creates database if it doesn't already exist.
# ${DB_COMMAND} 'CREATE DATABASE ${DB_NAME} WITH ENCODING "UTF8";'
	psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}';" | grep -q 1 || psql -U postgres -c "CREATE DATABASE ${DB_NAME} WITH ENCODING '${ENCODING}';" && echo "Database ${DB_NAME} created."
create_users:
# Option 1 - Create user and get input from to enter and repeat password. Echo command entered.
#	createuser -P -e ${DB_USER}
# Option 2 - Create user and set password as separate commands.
#   2.a - Create User
	${DB_COMMAND} "CREATE USER ${DB_USER};" && echo "User ${DB_USER} created."
#   2.b - Set Password
#     2.b.i - Get input from user for password using a different syntax. For some reason, enclosing escaped makefile var, e.g. '$$var' in single quotes causes nothing to appear in its place.
# read -s -p "Enter password for '${DB_USER}': " pwd; \
# ${DB_COMMAND} "ALTER USER ${DB_USER} WITH PASSWORD '$$pwd';"
#     2.b.ii. - Create PW automatically and have it replaced later.
	${DB_COMMAND} "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PW}';"
set_privileges:
	${DB_COMMAND} "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"
export_vars:
# export DATABASE_URL=postgres://${DB_USER}:${DB_PW}@localhost/${DB_NAME}
	export DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PW}@localhost/${DB_NAME}"

# Ad Hoc Tests
model: model_to_sqlalchemy
model_to_sqlalchemy:
	${PYTHON} -m pmaapi.api.open_model.open_model_py
