# With credit to Sierra Moxon: https://github.com/geneontology/go-fastapi/blob/main/Makefile
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help


prod: install export-requirements docker-build docker-run


docker-run:
	docker compose up -d

docker-build:
	docker build -t oai-monarch-plugin:latest .

start-prod:
	# OAI_PLUGIN_HOST_PORT is set in the docker-compose.yml for production
	poetry run gunicorn oai_monarch_plugin.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

dev: install start-dev

start-dev:
	OAI_PLUGIN_HOST_PORT=http://localhost:3434 poetry run uvicorn oai_monarch_plugin.main:app --host 0.0.0.0 --port 3434 --reload

test:
	poetry run pytest -v tests --capture=no

queries:
	echo "Testing Search"
	curl -X GET "http://localhost:3434/search?term=COVID-19&category=disease&rows=2"

	echo -e "\n\nTesting diseease -> gene associations"
	curl -X GET "http://localhost:3434/disease-genes?disease_id=MONDO:0019391&max_results=10&association_type=both"

	echo -e "\n\nTesting diseease -> phenotype associations"
	curl -X GET "http://localhost:3434/disease-phenotypes?disease_id=MONDO:0019391&phenotypes&rows=2"	



export-requirements:
	poetry export -f requirements.txt --output requirements.txt

install:
	poetry install



help:
	@echo ""
	@echo "DEV:"
	@echo "  make dev -- installs requirements, runs hot-restart dev server"
	@echo "  make test -- runs tests"
	@echo "  make queries -- runs tests against dev server (not via pytest, assumes dev server is running)"
	@echo "  "
	@echo "PROD:"
	@echo "  make prod -- installs requirements, exports requirements.txt, builds and runs dockerized prod server"
	@echo "  make docker-build -- build docker container"
	@echo "  make docker-run -- run make start-prod in docker via docker-compose"
	@echo "  make start-prod -- runs production server"
	@echo "  "
	@echo "ETC:"
	@echo "  make install -- run poetry install"
	@echo "  make export-requirements -- exports requirements.txt"
	@echo "  make help -- show this help"
	@echo ""