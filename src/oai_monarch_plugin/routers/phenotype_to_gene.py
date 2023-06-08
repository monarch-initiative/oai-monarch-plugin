from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field
from .models import *
from .utils import get_association_all
from .config import settings

BASE_API_URL = settings.monarch_api_url

router = APIRouter()

##############################
### Phenotype -> Gene endpoint
##############################

@router.get("/phenotype-genes",
            response_model=GeneAssociations,
            description="Get a list of genes associated with a phenotype",
            summary="Get a list of genes associated with a phenotype",
            response_description="A GeneAssociations object containing a list of GeneAssociation objects",
            operation_id="get_phenotype_gene_associations")
async def get_phenotype_gene_associations(phenotype_id: str = Query(..., description="The ontology identifier of the phenotype.", example="HP:0002721"),
                                                limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
                                                offset: Optional[int] = Query(1, description="Offset for pagination of results")) -> GeneAssociations:
        
        genericAssociations = await get_association_all(category = "biolink:GeneToPhenotypicFeatureAssociation", 
                                                entity = phenotype_id, 
                                                limit = limit, 
                                                offset = offset)
    
        associations = []
        for item in genericAssociations.get("items", []):
            gene = Gene(
                # in a GeneToPhenotypicFeatureAssociation, the gene is the subject
                id=item.get("subject"),
                label=item.get("subject_label")
            )
            assoc = GeneAssociation(
                    id=item.get("id"),
                    gene=gene
                )
            associations.append(assoc)
    
    
        return GeneAssociations(associations = associations, total = genericAssociations.get("total", 0))