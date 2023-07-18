from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from .config import settings
from .models import *
from .utils import get_association_all

BASE_API_URL = settings.monarch_api_url

router = APIRouter()

#################################
### Phenotype -> Disease endpoint
#################################


@router.get(
    "/phenotype-diseases",
    response_model=DiseaseAssociations,
    description="Get a list of diseases associated with a phenotype",
    summary="Get a list of diseases associated with a phenotype",
    response_description="A DiseaseAssociations object containing a list of DiseaseAssociation objects",
    operation_id="get_phenotype_disease_associations",
)
async def get_phenotype_disease_associations(
    phenotype_id: str = Query(
        ..., description="The ontology identifier of the phenotype.", example="HP:0002721"
    ),
    limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
    offset: Optional[int] = Query(0, description="Offset for pagination of results"),
) -> DiseaseAssociations:
    genericAssociations = await get_association_all(
        category="biolink:DiseaseToPhenotypicFeatureAssociation",
        entity=phenotype_id,
        limit=limit,
        offset=offset,
    )

    associations = []
    for item in genericAssociations.get("items", []):
        disease = Disease(
            # in a DiseaseToPhenotypicFeatureAssociation, the disease is the subject
            disease_id=item.get("subject"),
            label=item.get("subject_label"),
        )
        assoc = DiseaseAssociation(disease=disease)
        associations.append(assoc)

    return DiseaseAssociations(associations = associations, 
                               total = genericAssociations.get("total", 0),
                               disease_url_template = settings.monarch_ui_url + "/disease/{disease_id}")
