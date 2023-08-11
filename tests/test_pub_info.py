from oai_monarch_plugin.routers.utils import get_pub_info

def test_get_pub_info():
    id = "OMIM:180849"
    pub_info = get_pub_info(id)
    assert pub_info["id"] == id
    assert pub_info["url"] == "https://www.omim.org/entry/180849"
    assert pub_info["title"] == "OMIM Record"

    id = "ISBN-13:978-0721606156"
    pub_info = get_pub_info(id)
    assert pub_info["id"] == id
    assert pub_info["title"] == "Smith's Recognizable Patterns Of Human Malformation"
    assert pub_info["author(s)"] == "Kenneth Lyons Jones et al."
    assert pub_info["year"] == "2006"
    assert pub_info["publisher"] == "Saunders"
    assert pub_info["url"] == "https://openlibrary.org/isbn/9780721606156"

    id = "PMID:19204439"
    pub_info = get_pub_info(id)
    assert pub_info["id"] == id
    assert pub_info["title"] == "Rubinstein Taybi syndrome with hepatic hemangioma."
    assert pub_info["author(s)"] == "Sahiner UM et al."
    assert pub_info["year"] == "2009"
    assert pub_info["journal"] == "Med Princ Pract"
    assert pub_info["url"] == "https://pubmed.ncbi.nlm.nih.gov/19204439"
