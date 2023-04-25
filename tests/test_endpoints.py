import requests
import json
import pytest

import subprocess
import time
import shlex

@pytest.fixture(scope="module", autouse=True)  # Change the scope to "module"
def start_server():
    print("Starting server...")  # Optional: Add this line for debugging
    server_command = "uvicorn oai_monarch_plugin.main:app --host 0.0.0.0 --port 3333"
    server_process = subprocess.Popen(shlex.split(server_command))

    # Give the server some time to start before running the tests
    time.sleep(0.5)

    yield

    # Clean up the server process after tests have run
    server_process.terminate()
    server_process.wait()



BASE_URL = "http://localhost:3333"

#dev = "uvicorn oai_monarch_plugin.main:app --host 0.0.0.0 --port 3333 --reload"
#dev = "python:uvicorn.main.run(app='oai_monarch_plugin.main:app', host='0.0.0.0', port=3333, reload=True)"


@pytest.mark.usefixtures("start_server")
def test_search_endpoint():
    response = requests.get(f"{BASE_URL}/search/entity/COVID-19?category=disease&rows=2")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2


@pytest.mark.usefixtures("start_server")
def test_disease_gene_associations_endpoint():
    response = requests.get(f"{BASE_URL}/bioentity/disease/DOID:678/genes?max_results=10&association_type=both")
    assert response.status_code == 200
    data = response.json()
    assert "genes" in data
    assert len(data["genes"]) == 10
    for gene in data["genes"]:
        assert "gene_id" in gene
        assert "gene_label" in gene
        assert "relation_label" in gene


@pytest.mark.usefixtures("start_server")
def test_disease_phenotype_associations_endpoint():
    response = requests.get(f"{BASE_URL}/bioentity/disease/MONDO:0017309/phenotypes?rows=2")
    assert response.status_code == 200
    data = response.json()
    assert "associations" in data
    assert "numFound" in data
    assert len(data["associations"]) == 2
    for association in data["associations"]:
        assert "id" in association
        assert "frequency" in association
        assert "onset" in association
        assert "phenotype" in association
        assert "id" in association["phenotype"]
        assert "label" in association["phenotype"]
        assert association["onset"]["id"] is None or isinstance(association["onset"]["id"], str)
        assert association["onset"]["label"] is None or isinstance(association["onset"]["label"], str)


if __name__ == "__main__":
    pytest.main()
