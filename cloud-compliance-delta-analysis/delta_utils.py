# =============================================================================
#  delta_utils.py  --  Delta Analysis Utility Functions
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Provides utility functions for comparing two system state JSON objects.
#    - Designed for use by the Delta Analysis microservice (see app.py).
#
#  MAIN FUNCTION:
#    - compare_jsons(pre, post)
#        Compares 'pre' and 'post' (both dicts), reporting what passed, failed,
#        and a breakdown of all changes. Computes a pass percentage.
#
#  HOW IT WORKS:
#    - All keys in either JSON are checked.
#    - If the value for a key is unchanged, it is marked as "passed".
#    - If the value changed, the field is "failed" and its before/after values are recorded.
#    - Outputs a dict with all this info (used for reporting/UI/export).
# =============================================================================

def compare_jsons(pre, post):
    """
    Compare two JSON/dict objects and summarize:
      - Which fields are unchanged ("passed")
      - Which fields have changed ("failed")
      - For changed fields, record before/after values
      - Compute overall pass percentage
    Args:
        pre (dict): System state before remediation
        post (dict): System state after remediation
    Returns:
        dict: {passed, failed, changes, pass_pct}
    """
    passed, failed, changes = [], [], []
    # Combine all keys found in either input dict
    all_keys = set(pre.keys()) | set(post.keys())
    for k in all_keys:
        pre_val = pre.get(k)
        post_val = post.get(k)
        if pre_val == post_val:
            passed.append(k)  # Field unchanged
        else:
            failed.append(k)  # Field changed
            changes.append({"field": k, "before": pre_val, "after": post_val})
    pass_pct = round(100 * len(passed) / max(1, len(all_keys)), 1)  # Avoid div/0
    return {
        "passed": passed,
        "failed": failed,
        "changes": changes,
        "pass_pct": pass_pct
    }

# =============================================================================
#  End of delta_utils.py (Core compare logic for delta reporting)
# =============================================================================
