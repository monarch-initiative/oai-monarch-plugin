from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from .config import settings
from .models import *
from .utils import get_association_all, get_pub_info

BASE_API_URL = settings.monarch_api_url

router = APIRouter()

############################
### Gene -> Disease endpoint
############################


@router.get(
    "/gene-diseases",
    response_model=DiseaseAssociations,
    description="Get a list of diseases associated with a gene",
    summary="Get a list of diseases associated with a gene",
    response_description="A DiseaseAssociations object containing a list of DiseaseAssociation objects",
    operation_id="get_gene_disease_associations",
)
async def get_gene_disease_associations(
    gene_id: str = Query(..., description="The identifier of the gene.", example="HGNC:1884"),
    limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
    offset: Optional[int] = Query(0, description="Offset for pagination of results"),
) -> DiseaseAssociations:
    
    causalAssociations = await get_association_all(
        category="biolink:CausalGeneToDiseaseAssociation",
        entity=gene_id,
        limit=limit,
        offset=offset,
    )

    correlatedAssociations = await get_association_all(
        category="biolink:CorrelatedGeneToDiseaseAssociation",
        entity=gene_id,
        limit=limit,
        offset=offset,
    )


    associations = []
    for item in causalAssociations.get("items", []):
        disease = Disease(disease_id=item.get("object"), label=item.get("object_label"), type="causal")
        assoc = DiseaseAssociation(disease=disease, metadata={"relationship": "causal"})
        associations.append(assoc)

    for item in correlatedAssociations.get("items", []):
        disease = Disease(disease_id=item.get("object"), label=item.get("object_label"))
        assoc = DiseaseAssociation(disease=disease, metadata={"relationship": "correlated"})

        for pub in item.get("publications", []):
            assoc.publications.append(get_pub_info(pub))
            
        associations.append(assoc)


    return DiseaseAssociations(associations=associations, 
                               total=causalAssociations.get("total", 0) + correlatedAssociations.get("total", 0),
                               disease_url_template = settings.monarch_ui_url + "/disease/{disease_id}")
