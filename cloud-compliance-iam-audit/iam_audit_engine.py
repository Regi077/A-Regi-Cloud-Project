# Supports both privileges string and permissions array, includes least privilege, 
# overprovisioned, MFA, and color-coded support on frontend)

def audit_iam(iam_json):
    results = []
    high, medium, low = 0, 0, 0

    # --- User checks ---
    if "users" in iam_json:
        for user in iam_json["users"]:
            username = user.get("username", "")
            privileges = user.get("privileges", "")
            permissions = user.get("permissions", [])

            # Rule 1: Root user without MFA
            if username == "root" and not user.get("mfa_enabled", False):
                results.append({"risk": "High", "issue": "Root user has no MFA enabled"})
                high += 1

            # Rule 2: Overprivileged user (by privilege string)
            if privileges == "admin":
                results.append({"risk": "Medium", "issue": f"User {username} has admin privileges"})
                medium += 1

            # Rule 3: Overprivileged user (by permissions array, checks for '*' or 'admin')
            if isinstance(permissions, list):
                if "*" in permissions or "admin" in permissions:
                    results.append({"risk": "Medium", "issue": f"User {username} has overprivileged permissions ('*' or 'admin')"})
                    medium += 1

                # Rule 4: Least privilege – too many permissions (e.g., >10)
                if len(permissions) > 10:
                    results.append({"risk": "Low", "issue": f"User {username} has too many permissions ({len(permissions)})"})
                    low += 1

    # --- Group checks ---
    if "groups" in iam_json:
        for group in iam_json["groups"]:
            group_name = group.get("name", "")
            privileges = group.get("privileges", "")
            permissions = group.get("permissions", [])

            # Rule 5: Overprivileged group by privilege string
            if privileges == "admin":
                results.append({"risk": "Medium", "issue": f"Group {group_name} has admin privileges"})
                medium += 1

            # Rule 6: Overprivileged group by permissions array
            if isinstance(permissions, list):
                if "*" in permissions or "admin" in permissions:
                    results.append({"risk": "Medium", "issue": f"Group {group_name} has overprivileged permissions ('*' or 'admin')"})
                    medium += 1

                # Rule 7: Least privilege – too many permissions
                if len(permissions) > 10:
                    results.append({"risk": "Low", "issue": f"Group {group_name} has too many permissions ({len(permissions)})"})
                    low += 1

            # Rule 8: Full access policy (classic)
            if group.get("policy") == "full_access":
                results.append({"risk": "Medium", "issue": f"Group {group_name} has full access policy"})
                medium += 1

    # --- Risk scoring summary ---
    summary = {
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "details": results
    }
    return summary
