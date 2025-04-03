from src.knowledge_graph.build_graph import add_gene_disease_relationship
from config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Sample data to import
relationships = [
    {"gene": "TP53", "disease": "Lung Cancer"},
    {"gene": "KRAS", "disease": "Colorectal Cancer"}
]

# Add data to graph
for rel in relationships:
    add_gene_disease_relationship(driver, rel["gene"], rel["disease"])

print("✅ Data successfully imported into Neo4j.")
