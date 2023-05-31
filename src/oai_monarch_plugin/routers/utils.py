import httpx


async def get_association_all(category: str, entity: str, limit: int, offset: int) -> dict:
    """Get associations for a given category and entity.
    The response will be a list of dictionaries with entries for id, subject, subject_label, predicate, object, object_label, relation_label, frequency_qualifier, and onset_qualifier."""
    api_url = f"https://api-dev.monarchinitiative.org/v3/api/association/all"

    params = {
        "category": category,
        "entity": entity,
        "limit": limit,
        "offset": offset
    }

    async with httpx.AsyncClient() as client:
        #print("Calling: " + str(client.build_request("GET", api_url, params=params).url))
        response = await client.get(api_url, params=params)

    response_json = response.json()
    return response_json