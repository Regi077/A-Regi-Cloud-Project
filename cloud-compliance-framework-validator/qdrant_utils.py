from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"
COLLECTION = "compliance_rules"

def get_rules_from_qdrant(framework_name):
    client = QdrantClient(url=QDRANT_URL)
    # Mock query: fetch all rules for the selected framework
    # For now, just return all points and filter by framework if available
    results = client.scroll(collection_name=COLLECTION, scroll_filter=None, limit=100)
    rules = []
    for p in results[0]:
        payload = p.payload
        if "framework" in payload and payload["framework"] == framework_name:
            rules.append(payload)
        elif "framework" not in payload:
            rules.append(payload)  # fallback if not tagged
    return rules
