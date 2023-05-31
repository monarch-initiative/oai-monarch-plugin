from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

router = APIRouter()

#######################
### Search endpoint
#######################

# Define the models for search results
class SearchResultItem(BaseModel):
    id: str = Field(..., description="The ontology identifier of the search result.")
    name: str = Field(..., description="The name of the search result.")
    category: List[str] = Field(..., description="The categories of the search result.")
    description: Optional[str] = Field(None, description="The description of the search result.")

class SearchResultResponse(BaseModel):
    results: List[SearchResultItem] = Field(..., description="The list of search results.")

@router.get("/search",
         response_model=SearchResultResponse,
         description="Search for entities in the Monarch knowledge graph",
         summary="Search for entities in the Monarch knowledge graph",
         response_description="Search results for the given ontology term",
         operation_id="search_entity")
async def search_entity(term: str = Query(..., description="The ontology term to search for."),
                        category: Optional[str] = Query("biolink:Disease", description="The category to search within, as an array of strings. Valid categories are: biolink:Disease, biolink:PhenotypicQuality, and biolink:Gene"),
                        rows: Optional[int] = Query(2, description="The maximum number of search results to return.")) -> SearchResultResponse:
    
    api_url = f"{BASE_API_URL}/search"

    params = {
        "q": term,
        "category": category,
        "limit": rows
    }
    
    async with httpx.AsyncClient() as client:
        print(client.build_request("GET", api_url, params=params))
        response = await client.get(api_url, params=params)

    print(response.text)
    response_json = response.json()
    
    search_results = []
    for item in response_json.get("items", []):
        search_results.append(SearchResultItem(id=item.get("id"), name=item.get("name"), category=item.get("category"), description=item.get("description")))
    
    res = {"results": search_results}
    return res
