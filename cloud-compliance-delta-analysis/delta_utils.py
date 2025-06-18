
def compare_jsons(pre, post):
    passed, failed, changes = [], [], []
    all_keys = set(pre.keys()) | set(post.keys())
    for k in all_keys:
        pre_val = pre.get(k)
        post_val = post.get(k)
        if pre_val == post_val:
            passed.append(k)
        else:
            failed.append(k)
            changes.append({"field": k, "before": pre_val, "after": post_val})
    pass_pct = round(100 * len(passed) / max(1, len(all_keys)), 1)
    return {
        "passed": passed,
        "failed": failed,
        "changes": changes,
        "pass_pct": pass_pct
    }

