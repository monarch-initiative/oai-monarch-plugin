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
    description="Get information about entities",
    summary="Get information about entities",
    response_description="Information about the entities",
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

            entities.append(Entity(**response_json))
            
    return entities
