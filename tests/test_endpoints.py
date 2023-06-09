from fastapi.testclient import TestClient
import pytest

from oai_monarch_plugin.main import app  # replace with the actual path of your FastAPI app

test_client = TestClient(app)

def test_search_endpoint():
    response = test_client.get("/search?term=COVID-19&category=biolink:Disease&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2
    assert "total" in data
    
    for result in data["results"]:
        assert "id" in result
        assert "name" in result
        assert "categories" in result
        assert "description" in result


def test_gene_to_phenotype():
    response = test_client.get("/gene-phenotypes?gene_id=HGNC:1884&limit=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert len(data["associations"]) == 2, f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "id" in association
        assert "frequency_qualifier" in association
        assert "onset_qualifier" in association
        assert "phenotype" in association
        assert "id" in association["phenotype"]
        assert "label" in association["phenotype"]

def test_disease_to_gene():
    response = test_client.get("/disease-genes?disease_id=MONDO:0005148&limit=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert len(data["associations"]) == 2, f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "id" in association
        assert "gene" in association
        assert "id" in association["gene"]
        assert "label" in association["gene"]


def test_disease_to_phenotype():
    response = test_client.get("/disease-phenotypes?disease_id=MONDO:0005148&limit=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert len(data["associations"]) == 2, f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "id" in association
        assert "frequency_qualifier" in association
        assert "onset_qualifier" in association
        assert "phenotype" in association
        assert "id" in association["phenotype"]
        assert "label" in association["phenotype"]


def test_gene_to_disease():
    response = test_client.get("/gene-diseases?gene_id=HGNC:1884&limit=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert len(data["associations"]) == 1, f"Expected 1 association but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "id" in association
        assert "disease" in association
        assert "id" in association["disease"]
        assert "label" in association["disease"]


def test_phenotype_to_disease():
    response = test_client.get("/phenotype-diseases?phenotype_id=HP:0002721&limit=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert len(data["associations"]) == 2, f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "id" in association
        assert "disease" in association
        assert "id" in association["disease"]
        assert "label" in association["disease"]

def test_phenotype_to_gene():
    response = test_client.get("/phenotype-genes?phenotype_id=HP:0002721&limit=2")
    print(response.text)

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert len(data["associations"]) == 2, f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "id" in association
        assert "gene" in association
        assert "id" in association["gene"]
        assert "label" in association["gene"]


if __name__ == "__main__":
    pytest.main()
