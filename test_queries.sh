#!/usr/bin/env bash

echo "Testing Search"
curl -X GET "http://localhost:3434/search?term=COVID-19&category=disease&rows=2"

echo -e "\n\nTesting diseease -> gene associations"
curl -X GET "http://localhost:3434/disease-genes?disease_id=DOID:678&max_results=10&association_type=both"

echo -e "\n\nTesting diseease -> phenotype associations"
curl -X GET "http://localhost:3434/disease-phenotypes?disease_id=MONDO:0017309&phenotypes&rows=2"


