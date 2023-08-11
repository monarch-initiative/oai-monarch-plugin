from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from .config import settings
from .models import *
from .utils import get_association_all, get_pub_info

BASE_API_URL = settings.monarch_api_url

router = APIRouter()

##############################
### Phenotype -> Gene endpoint
##############################


@router.get(
    "/phenotype-genes",
    response_model=GeneAssociations,
    description="Get a list of genes associated with a phenotype",
    summary="Get a list of genes associated with a phenotype",
    response_description="A GeneAssociations object containing a list of GeneAssociation objects",
    operation_id="get_phenotype_gene_associations",
)
async def get_phenotype_gene_associations(
    phenotype_id: str = Query(
        ..., description="The ontology identifier of the phenotype.", example="HP:0002721"
    ),
    limit: Optional[int] = Query(10, description="The maximum number of associations to return."),
    offset: Optional[int] = Query(1, description="Offset for pagination of results"),
) -> GeneAssociations:
    genericAssociations = await get_association_all(
        category="biolink:GeneToPhenotypicFeatureAssociation",
        entity=phenotype_id,
        limit=limit,
        offset=offset,
    )

    associations = []
    for item in genericAssociations.get("items", []):
        gene = Gene(
            # in a GeneToPhenotypicFeatureAssociation, the gene is the subject
            gene_id=item.get("subject"),
            label=item.get("subject_label"),
        )
        assoc = GeneAssociation(gene=gene)

        for pub in item.get("publications", []):
            assoc.publications.append(get_pub_info(pub))

        associations.append(assoc)

    return GeneAssociations(associations=associations, 
                            total=genericAssociations.get("total", 0),
                            gene_url_template = settings.monarch_ui_url + "/gene/{gene_id}")
