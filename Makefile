# With credit to Sierra Moxon: https://github.com/geneontology/go-fastapi/blob/main/Makefile
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

all: install export-requirements start

dev: install start-dev

start:
	poetry run gunicorn oai_monarch_plugin.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

start-dev:
	poetry run uvicorn oai_monarch_plugin.main:app --host 0.0.0.0 --port 3434 --reload

test:
	poetry run pytest -v tests --capture=no

export-requirements:
	poetry export -f requirements.txt --output requirements.txt

install:
	poetry install

queries:
	echo "Testing Search"
	curl -X GET "http://localhost:3434/search?term=COVID-19&category=disease&rows=2"

	echo -e "\n\nTesting diseease -> gene associations"
	curl -X GET "http://localhost:3434/disease-genes?disease_id=MONDO:0019391&max_results=10&association_type=both"

	echo -e "\n\nTesting diseease -> phenotype associations"
	curl -X GET "http://localhost:3434/disease-phenotypes?disease_id=MONDO:0019391&phenotypes&rows=2"




help:
	@echo ""
	@echo "make all -- installs requirements, exports requirements.txt, runs production server"
	@echo "make dev -- installs requirements, runs hot-restart dev server"
	@echo "make test -- runs tests"
	@echo "make queries -- runs tests against dev server (not via pytest, assumes dev server is running)"
	@echo "make start -- runs production server"
	@echo "make start-dev -- runs hot-restart dev server"
	@echo "make export-requirements -- exports requirements.txt"
	@echo "make help -- show this help"
	@echo ""