import httpx
from loguru import logger

from .config import settings

BASE_API_URL = settings.monarch_api_url


async def get_association_all(category: str, entity: str, limit: int, offset: int) -> dict:
    """Get associations for a given category and entity.
    The response will be a list of dictionaries with entries for id, subject, subject_label, predicate, object, object_label, relation_label, frequency_qualifier, and onset_qualifier.
    """

    api_url = f"{BASE_API_URL}/association/all"

    params = {"category": category, "entity": entity, "limit": limit, "offset": offset}

    async with httpx.AsyncClient() as client:
        logger.info({
            "event": "monarch_api_call",
            "url": str(client.build_request("GET", api_url, params=params).url),
            "params": params,
            "api_url": api_url,
            "method": "GET"
        })
        
        response = await client.get(api_url, params=params)

    response_json = response.json()
    return response_json
