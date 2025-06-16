from qdrant_client import QdrantClient
import os

QDRANT_URL = "http://localhost:6333"
COLLECTION = "compliance_rules"

def upsert_rules_to_qdrant(rules):
    client = QdrantClient(url=QDRANT_URL)
    # Prepare data as simple points (mock - for real, add embedding vectors)
    # Create collection if it does not exist

    try:
        client.create_collection(COLLECTION, vectors_config={"size": 128, "distance": "Cosine"})
    except Exception:
        pass # Already exists

    points = []
    for idx, rule in enumerate(rules):
        points.append({
            "id": idx,
            "payload": rule,
            "vector": [0.0]*128   # placeholder
        })
    client.upsert(
        collection_name=COLLECTION,
        points=points
    )
    return "upserted" if points else "no points"
