# =============================================================================
#  iam_audit_engine.py  --  IAM Role/Policy Security Analysis Engine
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Evaluates IAM user and group objects for compliance with best practices.
#    - Flags common misconfigurations: no MFA for root, overprivileged roles,
#      violation of least privilege, and dangerous group policies.
#    - Returns a risk summary for UI (color-coded), plus detailed findings.
#
#  RULES IMPLEMENTED:
#    - Root user without MFA        (HIGH risk)
#    - Overprivileged user/group    (MEDIUM risk)
#    - Too many permissions         (LOW risk)
#    - Full access policy           (MEDIUM risk)
#
#  HOW TO USE:
#    - Call audit_iam(iam_json) with a dictionary containing "users" and "groups".
#    - Returns a summary with risk counts and a details list for UI reporting.
# =============================================================================

def audit_iam(iam_json):
    """
    Analyzes IAM configuration for risks and returns a color-coded summary.
    Supports both privilege strings and permissions arrays.
    Designed for cloud security audit automation.
    """
    results = []
    high, medium, low = 0, 0, 0

    # === User-level Security Checks ===
    if "users" in iam_json:
        for user in iam_json["users"]:
            username = user.get("username", "")
            privileges = user.get("privileges", "")
            permissions = user.get("permissions", [])

            # Rule 1: Root user without MFA (High risk)
            if username == "root" and not user.get("mfa_enabled", False):
                results.append({
                    "risk": "High",
                    "issue": "Root user has no MFA enabled"
                })
                high += 1

            # Rule 2: User with 'admin' privilege (Medium risk)
            if privileges == "admin":
                results.append({
                    "risk": "Medium",
                    "issue": f"User {username} has admin privileges"
                })
                medium += 1

            # Rule 3: User with '*' or 'admin' in permissions (Medium risk)
            if isinstance(permissions, list):
                if "*" in permissions or "admin" in permissions:
                    results.append({
                        "risk": "Medium",
                        "issue": f"User {username} has overprivileged permissions ('*' or 'admin')"
                    })
                    medium += 1

                # Rule 4: Too many permissions assigned (Low risk)
                if len(permissions) > 10:
                    results.append({
                        "risk": "Low",
                        "issue": f"User {username} has too many permissions ({len(permissions)})"
                    })
                    low += 1

    # === Group-level Security Checks ===
    if "groups" in iam_json:
        for group in iam_json["groups"]:
            group_name = group.get("name", "")
            privileges = group.get("privileges", "")
            permissions = group.get("permissions", [])

            # Rule 5: Group with 'admin' privilege (Medium risk)
            if privileges == "admin":
                results.append({
                    "risk": "Medium",
                    "issue": f"Group {group_name} has admin privileges"
                })
                medium += 1

            # Rule 6: Group with '*' or 'admin' in permissions (Medium risk)
            if isinstance(permissions, list):
                if "*" in permissions or "admin" in permissions:
                    results.append({
                        "risk": "Medium",
                        "issue": f"Group {group_name} has overprivileged permissions ('*' or 'admin')"
                    })
                    medium += 1

                # Rule 7: Group with too many permissions (Low risk)
                if len(permissions) > 10:
                    results.append({
                        "risk": "Low",
                        "issue": f"Group {group_name} has too many permissions ({len(permissions)})"
                    })
                    low += 1

            # Rule 8: Group with 'full_access' policy (Medium risk)
            if group.get("policy") == "full_access":
                results.append({
                    "risk": "Medium",
                    "issue": f"Group {group_name} has full access policy"
                })
                medium += 1

    # === Risk Scoring and Summary for UI Consumption ===
    summary = {
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "details": results  # List of all issues found, for color-coded dashboard display
    }
    return summary

# =============================================================================
#  End of iam_audit_engine.py (Plug-and-play IAM security audit logic)
# =============================================================================
