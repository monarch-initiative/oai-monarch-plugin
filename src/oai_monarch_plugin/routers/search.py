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
    id: str = Field(..., description="The ontology identifier of the search result.", example="MONDO:0009061")
    name: str = Field(..., description="The name of the search result.", example="cystic fibrosis")
    categories: List[str] = Field(..., description="The categories of the search result.", example=["biolink:Disease"])
    description: Optional[str] = Field(None, description="The description of the search result.", example="Cystic fibrosis (CF) is a genetic disorder characterized by the production of sweat with a high salt content and mucus secretions with an abnormal viscosity.")

class SearchResultItems(BaseModel):
    results: List[SearchResultItem] = Field(..., description="A list of SearchResultItem objects.")
    total: int = Field(..., description="The total number of search results available.")

@router.get("/search",
         response_model=SearchResultItems,
         description="Search for entities in the Monarch knowledge graph",
         summary="Search for entities in the Monarch knowledge graph",
         response_description="Search results for the given ontology term",
         operation_id="search_entity")
async def search_entity(term: str = Query(..., description="The ontology term to search for."),
                        category: Optional[str] = Query("biolink:Disease", description="A single category to search within as a string. Valid categories are: biolink:Disease, biolink:PhenotypicQuality, and biolink:Gene", example="biolink:Disease"),
                        limit: Optional[int] = Query(10, description="The maximum number of search results to return."), 
                        offset: Optional[int] = Query(0, description="Offset for pagination of results")) -> SearchResultItems:
    
    api_url = f"{BASE_API_URL}/search"

    params = {
        "q": term,
        "category": category,
        "limit": limit,
        "offset": offset
    }
    
    async with httpx.AsyncClient() as client:
        print("Calling: " + str(client.build_request("GET", api_url, params=params).url))
        response = await client.get(api_url, params=params)

    response_json = response.json()
    
    search_results = []
    for item in response_json.get("items", []):
        print(item)
        search_results.append(SearchResultItem(id=item.get("id"), name=item.get("name"), categories=item.get("category"), description=item.get("description")))

    return SearchResultItems(results = search_results, total = response_json.get("total", 0))
