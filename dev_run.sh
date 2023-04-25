#!/bin/bash

poetry run uvicorn oai_monarch_plugin.main:app --host 0.0.0.0 --port 3333 --reload
