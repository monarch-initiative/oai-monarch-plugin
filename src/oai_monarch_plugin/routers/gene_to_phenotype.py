from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

router = APIRouter()

##############################
### Gene -> Phenotype endpoint
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

@router.get("/gene-phenotypes",
         response_model=PhenotypeAssociationResponse,
         description="Get phenotypes associated with gene",
         summary="Get phenotypes associated with gene",
         response_description="Phenotypes associated with gene",
         operation_id="get_gene_phenotype_associations")
async def get_gene_phenotype_associations(gene_id: str = Query(..., description="The ontology identifier of the gene."),
                                             rows: Optional[int] = 10,
                                             offset: Optional[int] = 1) -> PhenotypeAssociationResponse:
    
    api_url = f"{BASE_API_URL}/association/all"

    params = {
        "category": "biolink:GeneToPhenotypicFeatureAssociation",
        "entity": gene_id,
        "limit": rows,
        "offset": offset
    }

    async with httpx.AsyncClient() as client:
        print(client.build_request("GET", api_url, params=params))
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
