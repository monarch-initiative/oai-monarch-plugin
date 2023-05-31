from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

router = APIRouter()


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
@router.get("/disease-genes",
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