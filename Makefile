.PHONY: all install migrate pep8 reset-db run runcelery runserver setup-db test upgrade

ENV=ve

all: install setup-db upgrade run

install:
	[ ! -d $(ENV)/ ] && python3.6 -m venv $(ENV)/ || :
	[ ! -f ".env" ] && cp dev.env .env || :
	$(ENV)/bin/pip install -r requirements.txt

migrate:
	FLASK_APP=main.py $(ENV)/bin/flask db migrate

upgrade:
	FLASK_APP=main.py $(ENV)/bin/flask db upgrade

pep8:
	$(ENV)/bin/autopep8 --in-place --recursive --a --a .

reset-db:
	dropdb bridge_server
	dropuser originprotocol
	$(MAKE) setup-db

run:
	$(MAKE) -j2 runserver runcelery

runcelery:
	$(ENV)/bin/celery -A util.tasks beat
	$(ENV)/bin/celery -A util.tasks worker -c=1

runserver:
		$(ENV)/bin/python main.py

setup-db:
	createdb bridge_server
	psql -c "\
		CREATE ROLE originprotocol WITH LOGIN CREATEDB PASSWORD 'originprotocol';\
		ALTER DATABASE bridge_server OWNER TO originprotocol;\
	"

test:
	$(ENV)/bin/pytest --flakes --codestyle
