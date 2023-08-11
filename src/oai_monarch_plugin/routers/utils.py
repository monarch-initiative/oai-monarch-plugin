import httpx
from loguru import logger
import eutils
from isbnlib import canonical, meta

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


def get_pub_info(pub: str) -> dict:
    """Get publication information for a given publication ID.
    The response will be a dictionary with entries for id, url, and title.
    """

    pub_dict = {"id": pub}

    if pub.startswith("ISBN"):
        logger.info({
            "event": "isbn_lookup",
            "id": pub
        })

        canonical_isbn = canonical(pub.split(':')[1])
        data = meta(canonical_isbn)

        authors = data.get("Authors", [None])
        author = None
        if len(authors) == 1:
            author = authors[0]
        else:
            author = authors[0] + " et al."

        pub_dict.update({
            "title": data.get("Title", None),
            "author(s)": author,
            "year": data.get("Year", None),
            "publisher": data.get("Publisher", None),
            "url": f"https://openlibrary.org/isbn/{canonical_isbn}"
        })


    elif pub.startswith("OMIM"):
        pub_dict["url"] = f"https://www.omim.org/entry/{pub.split(':')[1]}"
        pub_dict["title"] = "OMIM Record"


    elif pub.startswith("PMID"):
        logger.info({
            "event": "pubmed_lookup",
            "id": pub
        })

        ec = eutils.Client(api_key = settings.ncbi_api_key)
        pmid = pub.split(':')[1]
        data = next(iter(ec.efetch(db='pubmed', id = pmid)))

        authors = data.authors
        author = None
        if len(authors) == 1:
            author = authors[0]
        else:
            author = authors[0] + " et al."

        pub_dict.update({
            "title": data.title,
            "author(s)": author,
            "year": data.year,
            "journal": data.jrnl,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
        })
        print(pub_dict)
        
    return pub_dict