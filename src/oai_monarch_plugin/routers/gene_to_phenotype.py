from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field
from .models import *
from .utils import get_association_all

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

router = APIRouter()

##############################
### Gene -> Phenotype endpoint
##############################

@router.get("/gene-phenotypes",
         response_model=PhenotypeAssociations,
         description="Get a list of phenotypes associated with a gene",
         summary="Get a list of phenotypes associated with a gene",
         response_description="A PhenotypeAssociations object containing a list of PhenotypeAssociation objects",
         operation_id="get_gene_phenotype_associations")
async def get_gene_phenotype_associations(gene_id: str = Query(..., description="The ontology identifier of the gene.", example="HGNC:1884"),
                                             limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
                                             offset: Optional[int] = Query(1, description="Offset for pagination of results")) -> PhenotypeAssociations:
    

    genericAssociations = await get_association_all(category = "biolink:GeneToPhenotypicFeatureAssociation", 
                                             entity = gene_id, 
                                             limit = limit, 
                                             offset = offset)

    associations = []
    for item in genericAssociations.get("items", []):
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


    return PhenotypeAssociations(associations = associations, total = genericAssociations.get("total", 0))