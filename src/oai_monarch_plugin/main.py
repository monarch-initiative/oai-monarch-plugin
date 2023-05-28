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
from .routers import search

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

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

app.include_router(search.router)



##############################
### Disease -> Phenotype endpoint
##############################

class Phenotype(BaseModel):
    id: str = Field(..., description="The ontology identifier of the phenotype.")
    label: str = Field(..., description="The human-readable label of the phenotype.")

class PhenotypeAssociation(BaseModel):
    id: str
    frequency_qualifier: Optional[str] = None
    onset_qualifier: Optional[str] = None
    phenotype: Phenotype

class PhenotypeAssociationResponse(BaseModel):
    associations: List[PhenotypeAssociation]
    numFound: int

@app.get("/disease-phenotypes",
         response_model=PhenotypeAssociationResponse,
         description="Get phenotypes associated with disease",
         summary="Get phenotypes associated with disease",
         response_description="Phenotypes associated with disease",
         operation_id="get_disease_phenotype_associations")
async def get_disease_phenotype_associations(disease_id: str = Query(..., description="The ontology identifier of the disease."),
                                             limit: Optional[int] = 10,
                                             offset: Optional[int] = 1) -> PhenotypeAssociationResponse:
    
    api_url = f"{BASE_API_URL}/association/all"

    params = {
        "category": "biolink:DiseaseToPhenotypicFeatureAssociation",
        "entity": disease_id,
        "limit": limit,
        "offset": offset
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)

    response_json = response.json()

    associations = []
    for item in response_json.get("items", []):
        phenotype = Phenotype(
            id=item.get("object"),
            label=item.get("object_label")
        )
        assoc = PhenotypeAssociation(
                id=item.get("id"),
                frequency_qualifier=item.get("frequency_qualifier"),
                onset_qualifier=item.get("onset_qualifier"),
                phenotype=phenotype
            )
        associations.append(assoc)

    num_found = response_json.get("total", 0)
    res = {"associations": associations, "numFound": num_found}

    return res




##############################
### Disease -> Gene endpoint
##############################


# Define the models for gene information
class GeneInfo(BaseModel):
    gene_id: str = Field(..., description="The ontology identifier of the gene.")
    gene_label: str = Field(..., description="The human-readable label of the gene.")
    relation_label: str = Field(..., description="The human-readable label of the relation between the gene and the disease.")

class GeneInfoResponse(BaseModel):
    genes: List[GeneInfo] = Field(..., description="The list of genes associated with the disease.")

# Define the route for the endpoint
@app.get("/disease-genes",
         response_model=GeneInfoResponse,
         description="Get a list of genes associated with a disease",
         summary="Get a list of genes associated with a disease",
         response_description="List of genes for a disease",
         operation_id="get_disease_gene_associations")
async def get_disease_gene_associations(disease_id: str = Query(..., description="The ontology identifier of the disease."),
                                        max_results: Optional[int] = Query(10, description="The maximum number of results to return.")) -> GeneInfoResponse:
    
    api_url = f"{BASE_API_URL}/association/all"
    params = {
        "category": "biolink:GeneToDiseaseAssociation",
        "entity": disease_id,
        "limit": max_results,
        "offset": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)

    response_json = response.json()

    gene_info = []
    for item in response_json.get("items", []):
        gene_id = item.get("subject")
        gene_label = item.get("subject_label")
        relation_label = item.get("predicate")
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

@app.get("/gene-phenotypes",
         response_model=GenePhenotypeAssociationResponse,
         description="Get phenotypes associated with gene",
         summary="Get phenotypes associated with gene",
         response_description="Phenotypes associated with gene",
         operation_id="get_gene_phenotype_associations")
async def get_gene_phenotype_associations(gene_id: str = Query(..., description="The gene ontology identifier."),
                                          rows: Optional[int] = 4,
                                          facet: Optional[bool] = False,
                                          unselect_evidence: Optional[bool] = True,
                                          exclude_automatic_assertions: Optional[bool] = False,
                                          fetch_objects: Optional[bool] = False,
                                          use_compact_associations: Optional[bool] = True,
                                          direct: Optional[bool] = False,
                                          direct_taxon: Optional[bool] = False) -> GenePhenotypeAssociationResponse:

    api_url = f"{BASE_API_URL}/bioentity/gene/{gene_id}/phenotypes"

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
