from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field
from .models import *
from .utils import get_association_all
from .config import settings

BASE_API_URL = settings.monarch_api_url

router = APIRouter()

############################
### Gene -> Disease endpoint
############################

@router.get("/gene-diseases",
            response_model=DiseaseAssociations,
            description="Get a list of diseases associated with a gene",
            summary="Get a list of diseases associated with a gene",
            response_description="A DiseaseAssociations object containing a list of DiseaseAssociation objects",
            operation_id="get_gene_disease_associations")
async def get_gene_disease_associations(gene_id: str = Query(..., description="The ontology identifier of the gene.", example="HGNC:1884"),
                                            limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
                                            offset: Optional[int] = Query(1, description="Offset for pagination of results")) -> DiseaseAssociations:
        
    
        genericAssociations = await get_association_all(category = "biolink:GeneToDiseaseAssociation", 
                                                entity = gene_id, 
                                                limit = limit, 
                                                offset = offset)
    
        associations = []
        for item in genericAssociations.get("items", []):
            disease = Disease(
                id=item.get("object"),
                label=item.get("object_label")
            )
            assoc = DiseaseAssociation(
                    id=item.get("id"),
                    disease=disease
                )
            associations.append(assoc)
    

        return DiseaseAssociations(associations = associations, total = genericAssociations.get("total", 0))