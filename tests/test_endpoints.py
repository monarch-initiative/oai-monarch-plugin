import pytest
from fastapi.testclient import TestClient

from oai_monarch_plugin.main import app  # replace with the actual path of your FastAPI app

test_client = TestClient(app)


def test_phenotype_profile_search_endpoint():
    response = test_client.get("/phenotype-profile-search?ids=HP:0001131&ids=HP:0000069&ids=HP:0002240&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
    assert len(data["matches"]) == 2
    assert "max_max_ic" in data

    for match in data["matches"]:
        assert "rank" in match
        assert "score" in match
        assert "type" in match
        assert "taxon" in match
        assert "id" in match
        assert "label" in match


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


def test_get_entities_endpoint():
    response = test_client.get("/entity?ids=MONDO:0005148&ids=MONDO:0009061")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    for entity in data:
        assert "id" in entity
        assert "category" in entity
        assert "name" in entity
        assert "description" in entity
        assert "association_counts" in entity

        for association_count in entity["association_counts"]:
            assert "label" in association_count
            assert "count" in association_count


def test_gene_to_phenotype():
    response = test_client.get("/gene-phenotypes?gene_id=HGNC:1884&limit=2")

    # Basic assertions
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()


    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert (
        len(data["associations"]) == 2
    ), f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "frequency_qualifier" in association
        assert "onset_qualifier" in association
        assert "phenotype" in association
        assert "phenotype_id" in association["phenotype"]
        assert "label" in association["phenotype"]


def test_disease_to_gene():
    response = test_client.get("/disease-genes?disease_id=MONDO:0005148&limit=2")

    # Basic assertions
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    ## NOTE TODO: this is currently incorrect because we query for causal and correlated together with the same limit applied to each.
    assert (
        len(data["associations"]) == 4
    ), f"Expected 4 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "gene" in association
        assert "gene_id" in association["gene"]
        assert "label" in association["gene"]


def test_disease_to_phenotype():
    response = test_client.get("/disease-phenotypes?disease_id=MONDO:0005148&limit=2")

    # Basic assertions
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert (
        len(data["associations"]) == 2
    ), f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "frequency_qualifier" in association
        assert "onset_qualifier" in association
        assert "phenotype" in association
        assert "phenotype_id" in association["phenotype"]
        assert "label" in association["phenotype"]


def test_gene_to_disease():
    response = test_client.get("/gene-diseases?gene_id=HGNC:11773&limit=2")

    # Basic assertions
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    ## NOTE TODO: this is currently incorrect because we query for causal and correlated together with the same limit applied to each.
    assert (
        len(data["associations"]) == 4
    ), f"Expected 1 association but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "disease" in association
        assert "disease_id" in association["disease"]
        assert "label" in association["disease"]


def test_phenotype_to_disease():
    response = test_client.get("/phenotype-diseases?phenotype_id=HP:0002721&limit=2")

    # Basic assertions
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert (
        len(data["associations"]) == 2
    ), f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "disease" in association
        assert "disease_id" in association["disease"]
        assert "label" in association["disease"]


def test_phenotype_to_gene():
    response = test_client.get("/phenotype-genes?phenotype_id=HP:0002721&limit=2")
    print(response.text)

    # Basic assertions
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "total" in data, "Response body did not contain expected 'total' field"

    # Check that the number of returned associations matches the limit parameter
    assert (
        len(data["associations"]) == 2
    ), f"Expected 2 associations but received {len(data['associations'])}"

    # Check structure of each association
    for association in data["associations"]:
        assert "gene" in association
        assert "gene_id" in association["gene"]
        assert "label" in association["gene"]


if __name__ == "__main__":
    pytest.main()
