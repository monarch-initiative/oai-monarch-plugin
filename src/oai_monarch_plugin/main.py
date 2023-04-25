# The following code provides a thin wrapper around the Monarch API
# to provide a simple API for the OpenAI plugin to use. It uses FastAPI
# and is run on port 3434 by default.


from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from os.path import abspath, dirname

BASE_API_URL = "https://api.monarchinitiative.org/api"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Serve static files needed for OpenAI plugin
app.mount("/.well-known", StaticFiles(directory = dirname(abspath(__file__)) + "/.well-known"), name="well-known")
app.mount("/static", StaticFiles(directory = dirname(abspath(__file__)) + "/static"), name="static")



#######################
### Search endpoint
#######################

# Define the models for search results
class SearchResultItem(BaseModel):
    id: str = Field(..., description="The ontology identifier of the search result.")
    synonyms: List[str] = Field(..., description="The list of synonyms for the search result.")

class SearchResultResponse(BaseModel):
    results: List[SearchResultItem] = Field(..., description="The list of search results.")

@app.get("/search/entity/{term}",
         response_model=SearchResultResponse,
         description="Search for entities in the Monarch knowledge graph",
         summary="Search for entities in the Monarch knowledge graph",
         response_description="Search results for the given ontology term",
         operation_id="search_entity")
async def search_entity(term: str = Path(..., description="The ontology term to search for."),
                        category: Optional[List[str]] = Query(["disease"], description="The category to search within."),
                        rows: Optional[int] = Query(2, description="The maximum number of search results to return.")) -> SearchResultResponse:
    
    api_url = f"{BASE_API_URL}/search/entity/{term}"
    
    params = {
        "category": category,
        "rows": rows
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)

    response_json = response.json()
    
    search_results = []
    for doc in response_json.get("docs", []):
        search_results.append(SearchResultItem(id=doc.get("id"), synonyms=doc.get("synonym", [])))
    
    res = {"results": search_results}
    print(res)
    return res





##############################
### Disease -> Phenotype endpoint
##############################

class Phenotype(BaseModel):
    id: str = Field(..., description="The ontology identifier of the phenotype.")
    label: str = Field(..., description="The human-readable label of the phenotype.")

class PhenotypeAssociation(BaseModel):
    id: str
    frequency: Dict[str, Optional[str]]
    onset: Dict[str, Optional[str]]
    phenotype: Phenotype

class PhenotypeAssociationResponse(BaseModel):
    associations: List[PhenotypeAssociation]
    numFound: int

@app.get("/bioentity/disease/{id}/phenotypes",
         response_model=PhenotypeAssociationResponse,
         description="Get phenotypes associated with disease",
         summary="Get phenotypes associated with disease",
         response_description="Phenotypes associated with disease",
         operation_id="get_disease_phenotype_associations")
async def get_disease_phenotype_associations(id: str,
                                             rows: Optional[int] = 10,
                                             unselect_evidence: Optional[bool] = True) -> PhenotypeAssociationResponse:
    
    api_url = f"{BASE_API_URL}/bioentity/disease/{id}/phenotypes"

    params = {
        "rows": rows,
        "unselect_evidence": unselect_evidence
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)

    response_json = response.json()

    associations = []
    for association in response_json.get("associations", []):
        phenotype = Phenotype(
            id=association.get("object", {}).get("id"),
            label=association.get("object", {}).get("label")
        )
        associations.append(
            PhenotypeAssociation(
                id=association.get("id"),
                frequency=association.get("frequency", {}),
                onset=association.get("onset", {}),
                phenotype=phenotype
            )
        )

    num_found = response_json.get("numFound", 0)

    return {"associations": associations, "numFound": num_found}




##############################
### Disease -> Gene endpoint
##############################

# Define the association types as an enumeration
class AssociationType(str, Enum):
    causal = "causal"
    non_causal = "non_causal"
    both = "both"

# Define the models for gene information
class GeneInfo(BaseModel):
    gene_id: str = Field(..., description="The ontology identifier of the gene.")
    gene_label: str = Field(..., description="The human-readable label of the gene.")
    relation_label: str = Field(..., description="The human-readable label of the relation between the gene and the disease.")

class GeneInfoResponse(BaseModel):
    genes: List[GeneInfo] = Field(..., description="The list of genes associated with the disease.")

# Define the route for the endpoint
@app.get("/bioentity/disease/{id}/genes",
         response_model=GeneInfoResponse,
         description="Get gene information for a disease",
         summary="Get gene information for a disease",
         response_description="Gene information for a disease",
         operation_id="get_disease_gene_associations")
async def get_disease_gene_associations(id: str = Path(..., description="The ontology identifier of the disease."),
                                        max_results: Optional[int] = Query(10, description="The maximum number of results to return."),
                                        association_type: AssociationType = Query(AssociationType.causal, description="The type of association to return.")) -> GeneInfoResponse:
    
    api_url = f"{BASE_API_URL}/bioentity/disease/{id}/genes"
    params = {
        "rows": max_results,
        "association_type": association_type.value  # Convert the enumeration value to a string
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)

    response_json = response.json()

    gene_info = []
    for association in response_json.get("associations", []):
        gene_id = association.get("object", {}).get("id")
        gene_label = association.get("object", {}).get("label")
        relation_label = association.get("relation", {}).get("label")
        if gene_id:
            gene_info.append({
                "gene_id": gene_id,
                "gene_label": gene_label,
                "relation_label": relation_label
            })

    return {"genes": gene_info}





##############################
### Gene -> Phenotype endpoint
##############################

class GenePhenotypeAssociation(BaseModel):
    subject: str = Field(..., description="The gene identifier.")
    relation: str = Field(..., description="The ontology identifier of the relation.")
    objects: List[str] = Field(..., description="A list of phenotype ontology identifiers associated with the gene.")

class GenePhenotypeAssociationResponse(BaseModel):
    compact_associations: List[GenePhenotypeAssociation]
    numFound: int

@app.get("/bioentity/gene/{id}/phenotypes",
         response_model=GenePhenotypeAssociationResponse,
         description="Get phenotypes associated with gene",
         summary="Get phenotypes associated with gene",
         response_description="Phenotypes associated with gene",
         operation_id="get_gene_phenotype_associations")
async def get_gene_phenotype_associations(id: str,
                                          rows: Optional[int] = 4,
                                          facet: Optional[bool] = False,
                                          unselect_evidence: Optional[bool] = True,
                                          exclude_automatic_assertions: Optional[bool] = False,
                                          fetch_objects: Optional[bool] = False,
                                          use_compact_associations: Optional[bool] = True,
                                          direct: Optional[bool] = False,
                                          direct_taxon: Optional[bool] = False) -> GenePhenotypeAssociationResponse:

    api_url = f"{BASE_API_URL}/bioentity/gene/{id}/phenotypes"

    params = {
        "rows": rows,
        "facet": facet,
        "unselect_evidence": unselect_evidence,
        "exclude_automatic_assertions": exclude_automatic_assertions,
        "fetch_objects": fetch_objects,
        "use_compact_associations": use_compact_associations,
        "direct": direct,
        "direct_taxon": direct_taxon
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)

    response_json = response.json()

    compact_associations = []
    for association in response_json.get("compact_associations", []):
        compact_associations.append(
            GenePhenotypeAssociation(
                subject=association.get("subject"),
                relation=association.get("relation"),
                objects=association.get("objects", [])
            )
        )

    num_found = response_json.get("numFound", 0)

    return {"compact_associations": compact_associations, "numFound": num_found}
