from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

router = APIRouter()

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

@router.get("/gene-phenotypes",
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
