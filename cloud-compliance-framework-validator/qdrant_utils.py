# =============================================================================
#  qdrant_utils.py  --  Utility Functions for Qdrant Vector DB Integration
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Provides helper functions to connect and query the Qdrant vector database.
#    - Used for fetching compliance rule embeddings relevant to a chosen framework.
#    - Qdrant stores each rule as a "point" (vector + payload metadata).
#
#  HOW IT WORKS:
#    - Connects to local Qdrant instance (URL, port 6333).
#    - Collection name defaults to "compliance_rules".
#    - Returns all rules that match the requested framework, or all if not tagged.
# =============================================================================

from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"   # Where your Qdrant DB is running (docker-compose)
COLLECTION = "compliance_rules"        # Standardized collection for all parsed rules

def get_rules_from_qdrant(framework_name):
    """
    Fetch all compliance rules from Qdrant that belong to the given framework.
    If a rule is not tagged with a framework, it will also be returned (fallback).
    
    Args:
        framework_name (str): The name of the compliance framework (e.g., "NIST 800-53").
    Returns:
        list[dict]: A list of rule payloads (each as a dict).
    """
    client = QdrantClient(url=QDRANT_URL)
    # For now: fetch all points, filter client-side (for demo/mock simplicity)
    results = client.scroll(collection_name=COLLECTION, scroll_filter=None, limit=100)
    rules = []
    for p in results[0]:  # results[0] is the list of points
        payload = p.payload
        # Only include rules for the selected framework (if tagged)
        if "framework" in payload and payload["framework"] == framework_name:
            rules.append(payload)
        # Fallback: include untagged rules (future-proofing for older data)
        elif "framework" not in payload:
            rules.append(payload)
    return rules

# =============================================================================
#  End of qdrant_utils.py (Qdrant DB connectivity and rules fetch helper)
# =============================================================================
