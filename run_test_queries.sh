#!/usr/bin/env bash

echo "Testing Search"
curl -X GET "http://localhost:3333/search/entity/COVID-19?category=disease&rows=2"


echo "Testing gene associations"
curl -X GET "http://localhost:3333/bioentity/disease/DOID%3A678/genes?max_results=10&association_type=both"