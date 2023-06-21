from typing import List, Optional

import httpx
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from loguru import logger

from .config import settings

BASE_API_URL = settings.monarch_api_v2_url

router = APIRouter()

# Define the models for search results
class MatchItem(BaseModel):
    rank: str = Field(..., description="The rank of the match, with 1 being the closest match.")
    score: int = Field(..., description="The score of the matching item using the phenodigm metric.")
    type: str = Field(..., description="The type of the matching item, e.g. disease or gene.")
    taxon: dict = Field(..., description="The taxon of the matching item as a dict with keys for id and label.")
    id: str = Field(..., description="The ontology identifier of the matching item.")
    label: str = Field(..., description="The human-readable label of the matching item.")


class MatchItems(BaseModel):
    matches: List[MatchItem] = Field(..., description="A list of MatchItem objects.")
    max_max_ic: float = Field(..., description="max_max_ic")


@router.get(
    "/phenotype-profile-search",
    response_model=MatchItems,
    description="Semantic similarity search, or fuzzy search, between genes and/or diseases.",
    summary="Allows fuzzy-matching of genes and/or diseases to each other. The input is provided as a list of genes and/or diseases from which associated phenotypes will be extracted and unioned.",
    response_description="Search results as an array of MatchItem objects.",
    operation_id="search_phenotype_profiles",
)
async def search_phenotype_profiles(
    ids: List[str] = Query(
        ..., 
        description="The ontology identifiers to search for as a list of gene and/or disease IDs."
    ),
    limit: Optional[int] = Query(10, description="The maximum number of search results to return."),
) -> MatchItems:
    api_url = f"{BASE_API_URL}/sim/search"
    
    is_feature_set = all('HP:' in id for id in ids)

    params = {"id": ids, "is_feature_set": is_feature_set, "metric": "phenodigm", "limit": limit}

    async with httpx.AsyncClient() as client:
        logger.info({
            "event": "monarch_api_call_v2",
            "url": str(client.build_request("GET", api_url, params=params).url),
            "params": params,
            "api_url": api_url,
            "method": "GET"
        })
        logger.info(f"params: {params}, url: {str(client.build_request('GET', api_url, params=params).url)}")
        response = await client.get(api_url, params=params)

    response_json = response.json()

    matches = []
    for item in response_json.get("matches", []):
        matches.append(
            MatchItem(
                rank=item.get("rank"),
                score=item.get("score"),
                type=item.get("type"),
                taxon=item.get("taxon"),
                id=item.get("id"),
                label=item.get("label"),
            )
        )

    return MatchItems(matches=matches, max_max_ic=response_json.get("metadata", {}).get("max_max_ic"))
