from Bio import Entrez
import os

# Setting email
Entrez.email = os.getenv("ENTREZ_EMAIL", "your_email@example.com")


def build_pubmed_query(terms, filters={}):
    """
    Construct a PubMed search query.

    :param terms: List of search terms (e.g., ["TP53", "lung cancer"])
    :param filters: Dictionary of additional filters (e.g., {"Title": True, "Publication Type": "Review"})
    :return: PubMed query string
    """
    query = " AND ".join(terms)

    # Apply filters
    filter_mappings = {
        "Title": "[Title]",
        "Abstract": "[Abstract]",
        "Title/Abstract": "[TIAB]",
        "Publication Type": "[PT]",
        "Journal": "[TA]",
        "Date": "[dp]"
    }

    for key, value in filters.items():
        if key in filter_mappings:
            if isinstance(value, list):
                query += " AND (" + " OR ".join([f"{v}{filter_mappings[key]}" for v in value]) + ")"
            else:
                query += f" AND {value}{filter_mappings[key]}"

    return query

def search_pubmed(query, max_results=10, order_by = "relevance"):
    """
    Search PubMed for articles matching the query.

    :param query: PubMed query string, single string or created by build_pubmed_query()
    :param max_results: Integer for max counts of PubMed IDs. Default is 10.
    :param order_by:  Default is "relevance", "pub+date" for sorting by most recent
    and "pubdate" for Sort by Publication Date (Oldest to Newest)
    """
    #object return xml format, need to use read() to read the object
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort = order_by)
    record = Entrez.read(handle)
    return record["IdList"], record["Count"]  # List of PMIDs


def fetch_pubmed_abstracts(pmids):
    """Retrieve abstracts for given PubMed IDs."""
    handle = Entrez.efetch(db="pubmed", id=pmids, rettype="abstract", retmode="text")
    return handle.read()


def get_pmc_full_text(pmid):
    """Check if full text is available in PubMed Central (PMC)."""
    handle = Entrez.elink(dbfrom="pubmed", id=pmid, linkname="pubmed_pmc")
    record = Entrez.read(handle)

    if "LinkSetDb" in record[0] and len(record[0]["LinkSetDb"]) > 0:
        pmc_id = record[0]["LinkSetDb"][0]["Link"][0]["Id"]
        return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/"
    return "No free full-text available."

# Example
#query = "crispr"


