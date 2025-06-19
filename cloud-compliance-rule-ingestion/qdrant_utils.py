# =============================================================================
#  qdrant_utils.py  --  Qdrant Vector DB Utility for Rule Upserts
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Handles interaction with the Qdrant vector database for storing and updating compliance rules.
#    - Used during rule ingestion (Phase 3) to persist LLM-extracted rules for later validation/search.
#
#  KEY FUNCTIONS:
#    - upsert_rules_to_qdrant(rules): Saves rules as vector points into the Qdrant collection.
#
#  DEPENDENCIES:
#    - qdrant-client (Python): Python SDK for Qdrant vector DB.
#
#  CONFIGURATION:
#    - QDRANT_URL: Read from environment or defaults to Docker Compose service name ('qdrant:6333').
#    - COLLECTION: Compliance rules collection name (default: 'compliance_rules').
# =============================================================================

from qdrant_client import QdrantClient
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLLECTION = os.getenv("QDRANT_COLLECTION", "compliance_rules")

# -----------------------------------------------------------------------------
#  upsert_rules_to_qdrant
# -----------------------------------------------------------------------------
def upsert_rules_to_qdrant(rules):
    """
    Upserts a list of compliance rules as vector points into the Qdrant database.
    - Each rule is stored as a payload; a dummy zero-vector is used for now.
    - Automatically creates the collection if it does not already exist.

    Args:
        rules (list[dict]): List of compliance rule dicts.

    Returns:
        str: "upserted" if points were written, "no points" if rules was empty.
    """
    client = QdrantClient(url=QDRANT_URL)
    # Ensure collection exists (creates if not)
    try:
        client.create_collection(
            COLLECTION,
            vectors_config={"size": 128, "distance": "Cosine"}  # 128-dim placeholder vectors
        )
    except Exception:
        pass  # Ignore if collection already exists

    points = []
    for idx, rule in enumerate(rules):
        points.append({
            "id": idx,              # Use index as a simple unique ID
            "payload": rule,        # Store the rule as the payload (searchable/filterable)
            "vector": [0.0] * 128   # Placeholder vector for now (for future embedding upgrades)
        })

    # Upsert all points into Qdrant collection
    if points:
        client.upsert(collection_name=COLLECTION, points=points)
        return "upserted"
    else:
        return "no points"

# =============================================================================
#  End of qdrant_utils.py (Handles upserting rules to vector DB)
# =============================================================================
