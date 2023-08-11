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
### Disease -> Gene endpoint
############################


@router.get(
    "/disease-genes",
    response_model=GeneAssociations,
    description="Get a list of genes associated with a disease",
    summary="Get a list of genes associated with a disease",
    response_description="A GeneAssociations object containing a list of GeneAssociation objects",
    operation_id="get_disease_gene_associations",
)
async def get_disease_gene_associations(
    disease_id: str = Query(
        ..., description="The ontology identifier of the disease.", example="MONDO:0009061"
    ),
    limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
    offset: Optional[int] = Query(0, description="Offset for pagination of results"),
) -> GeneAssociations:
    
    causalAssociations = await get_association_all(
        category="biolink:CausalGeneToDiseaseAssociation",
        entity=disease_id,
        limit=limit,
        offset=offset,
    )

    correlatedAssociations = await get_association_all(
        category="biolink:CorrelatedGeneToDiseaseAssociation",
        entity=disease_id,
        limit=limit,
        offset=offset,
    )

    associations = []

    for item in causalAssociations.get("items", []):
        gene = Gene(
            # in a GeneToDiseaseAssociation, the gene is the subject
            gene_id=item.get("subject"),
            label=item.get("subject_label"),
        )
        assoc = GeneAssociation(gene=gene, metadata={"relationship": "causal"})
        associations.append(assoc)

    for item in correlatedAssociations.get("items", []):
        gene = Gene(
            # in a GeneToDiseaseAssociation, the gene is the subject
            gene_id=item.get("subject"),
            label=item.get("subject_label"),
        )
        assoc = GeneAssociation(gene=gene, metadata={"relationship": "correlated"})

        for pub in item.get("publications", []):
            assoc.publications.append(get_pub_info(pub))

        associations.append(assoc)

    return GeneAssociations(associations = associations, 
                            total = causalAssociations.get("total", 0) + correlatedAssociations.get("total", 0),
                            gene_url_template = settings.monarch_ui_url + "/gene/{gene_id}")
