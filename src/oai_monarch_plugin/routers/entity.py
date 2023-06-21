from typing import List

import httpx
from fastapi import APIRouter, Query
from loguru import logger

from .config import settings
from .models import *

BASE_API_URL = settings.monarch_api_url

router = APIRouter()

@router.get(
    "/entity",
    response_model=List[Entity],
    description="Get information about arbitrary entities by identifier, e.g. MONDO:0005737, HP:0002721, HGNC:1884.",
    summary="Returns information on entities such as name, description, synonyms, categories, and counts of associations to other entities of different types.",
    response_description="A JSON array of entity descriptors.",
    operation_id="get_entities",
)
async def get_entities(ids: List[str] = Query(..., description="List of entity ids")) -> List[Entity]:
    entities = []
    async with httpx.AsyncClient() as client:
        for id in ids:
            api_url = f"{BASE_API_URL}/entity/{id}"
            logger.info({
                "event": "monarch_api_call",
                "url": str(client.build_request("GET", api_url).url),
                "api_url": api_url,
                "method": "GET"
            })

            response = await client.get(api_url)

            response_json = response.json()

            id = response_json.get("id")
            category = response_json.get("category")
            name = response_json.get("name")
            description = response_json.get("description")
            symbol = response_json.get("symbol")
            synonym = response_json.get("synonym")

            association_counts_json = response_json.get("association_counts")
            association_counts = []
            for association_count_json in association_counts_json:
                association_count: AssociationCount = AssociationCount(label = association_count_json.get("label"), 
                                                                       count = association_count_json.get("count"))
                association_counts.append(association_count)

            
            entities.append(Entity(id=id, category=category, name=name, description=description, symbol=symbol, synonym=synonym, association_counts=association_counts))
            
    return entities
