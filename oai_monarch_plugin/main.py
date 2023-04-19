from enum import Enum
from typing import List, Optional

import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_API_URL = "https://api.monarchinitiative.org/api"

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Serve static files needed for OpenAI plugin
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
app.mount("/static", StaticFiles(directory="static"), name="static")

#######################
### Disease endpoint
#######################

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
    genes: List[GeneInfo]

# Define the route for the endpoint
@app.get("/bioentity/disease/{id}/genes",
         response_model=GeneInfoResponse,
         description="Get gene information for a disease",
         summary="Get gene information for a disease",
         response_description="Gene information for a disease",
         operation_id="get_disease_gene_associations")
async def get_disease_gene_associations(
    id: str = "MONDO:0100096",
    max_results: Optional[int] = 10,
    association_type: AssociationType = AssociationType.both
) -> GeneInfoResponse:
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
async def search_entity(
    term: str,
    category: Optional[List[str]] = Query(["disease"], description="The category to search within."),
    rows: Optional[int] = Query(2, description="The maximum number of search results to return.")
) -> SearchResultResponse:
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
    
    return {"results": search_results}

