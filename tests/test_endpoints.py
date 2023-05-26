from fastapi.testclient import TestClient
import pytest

from oai_monarch_plugin.main import app  # replace with the actual path of your FastAPI app

test_client = TestClient(app)

def test_search_endpoint():
    response = test_client.get("/search?term=COVID-19&category=biolink:Disease&rows=2")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2

def test_disease_genes_endpoint():
    response = test_client.get("/disease-genes?disease_id=MONDO:0019391&max_results=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()
    print(data)

    # Check for presence of 'genes' in the response
    assert "genes" in data, "Response body did not contain expected 'genes' field"

    # Check that the number of returned genes matches the max_results parameter
    assert len(data["genes"]) == 2, f"Expected 2 genes but received {len(data['genes'])}"

    # Check structure of each gene
    for gene in data["genes"]:
        assert "gene_id" in gene
        assert "gene_label" in gene
        assert "relation_label" in gene

    # Ensure gene_id, gene_label, and relation_label are strings
    for gene in data['genes']:
        assert isinstance(gene['gene_id'], str), f"Expected 'gene_id' to be a string but found {type(gene['gene_id'])}"
        assert isinstance(gene['gene_label'], str), f"Expected 'gene_label' to be a string but found {type(gene['gene_label'])}"
        assert isinstance(gene['relation_label'], str), f"Expected 'relation_label' to be a string but found {type(gene['relation_label'])}"

def test_disease_phenotype_associations_endpoint():
    response = test_client.get("/disease-phenotypes?disease_id=MONDO:0017309&limit=2")

    # Basic assertions
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code} with message: {response.text}"

    # Ensure response is valid JSON
    data = response.json()

    # Check for presence of 'associations' and 'numFound' in the response
    assert "associations" in data, "Response body did not contain expected 'associations' field"
    assert "numFound" in data, "Response body did not contain expected 'numFound' field"

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

    # Check that numFound is an integer
    assert isinstance(data['numFound'], int), f"Expected 'numFound' to be an integer but found {type(data['numFound'])}"



if __name__ == "__main__":
    pytest.main()
