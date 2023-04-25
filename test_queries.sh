#!/usr/bin/env bash

echo "Testing Search"
curl -X GET "http://localhost:3434/search/entity/COVID-19?category=disease&rows=2"

echo -e "\n\nTesting diseease -> gene associations"
curl -X GET "http://localhost:3434/bioentity/disease/DOID:678/genes?max_results=10&association_type=both"

echo -e "\n\nTesting diseease -> phenotype associations"
curl -X GET "http://localhost:3434/bioentity/disease/MONDO:0017309/phenotypes?rows=2"


