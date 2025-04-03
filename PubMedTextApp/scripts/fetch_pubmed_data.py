import json
from src.data_ingestion.pubmed_api import search_pubmed, fetch_pubmed_abstracts

query = "Chronic Diseases"
# past 5 years publication ratio 
# cancer:Cardiovascular Diseases:Neurological Disorders:Infectious Diseases:Chronic Diseases
# 4:2:2:1:1 about 1M for cancer research
pmids = search_pubmed(query, max_results=50)[0]

articles = []
for pmid in pmids:
    abstract = fetch_pubmed_abstracts([pmid])
    articles.append({"pmid": pmid, "abstract": abstract})

# Save results to JSON
with open("../data_ouputs/pubmed_articles_chronict50.json", "w") as f:
    json.dump(articles, f, indent=4)

print("✅ Fetched and saved PubMed articles.")