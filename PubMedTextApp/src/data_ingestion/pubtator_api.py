import requests
import json
import pubmed_api
from pubmed_api import fetch_pubmed_abstracts

PUBTATOR_API_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids={}"

def fetch_pubtator_annotations(pmids):
    """Retrieve annotated biomedical entities from PubTator."""
    url = PUBTATOR_API_URL.format(",".join(pmids))
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def extract_gene_relationships(pubtator_data):
    """
    Extract functional relationships between genes from PubTator annotations.
    :param annotations: JSON response from PubTator
    :return: Dictionary of gene relationships
    """
    gene_relationships = {}

    for entry in pubtator_data.get("PubTator3", []):
        pmid = entry.get("id")
        for passage in entry.get("passages", []):
            for relation in passage.get("relations", []):
                infons = relation.get("infons", {})

                role1 = infons.get("role1", {})
                role2 = infons.get("role2", {})
                relationship_type = infons.get("type")
                score = infons.get("score", "N/A")

                role1_id = role1.get("identifier")
                role1_type = role1.get("type")
                role1_name = role1.get("name")

                role2_id = role2.get("identifier")
                role2_type = role2.get("type")
                role2_name = role2.get("name")

                # Ensure at least one entity is a gene
                if "Gene" in (role1_type, role2_type):
                    relationships.append({
                        "pmid": pmid,
                        "gene_id": role1_id if role1_type == "Gene" else role2_id,
                        "gene_name": role1_name if role1_type == "Gene" else role2_name,
                        "related_entity_id": role2_id if role1_type == "Gene" else role1_id,
                        "related_entity_name": role2_name if role1_type == "Gene" else role1_name,
                        "related_entity_type": role2_type if role1_type == "Gene" else role1_type,
                        "relationship_type": relationship_type,
                        "score": score
                    })

    return gene_relationships

#pmids = pubmed_api.search_pubmed("CRISPR", max_results=3)[0]
pmids = ["30049270", "29446767"]
pt_ann = fetch_pubtator_annotations(pmids)

if pt_ann:
        relationships = extract_gene_relationships(pt_ann)
        print(json.dumps(relationships, indent=2))
#print(pt_ann['PubTator3'][0])
#annotations = pt_ann['PubTator3'][0]

#for k, v in annotations.items():

#print(pt_ann)
#['annotations']




