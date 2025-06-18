# =============================================================================
#  audit.py  --  Simple Audit Logging Utility for Cloud Compliance API
# =============================================================================
#  PURPOSE:
#   - This module provides a reusable function to log security/audit events.
#   - Every important user/system action (e.g., login, config change, privileged call)
#     should be recorded for accountability and regulatory compliance.
#   - Logs both to stdout (for real-time monitoring) and to an audit.log file (for traceability).
#
#  HOW TO USE:
#   - Call audit_log(action, user, details) from anywhere in the API when a sensitive
#     operation occurs. Pass in a string 'action' and the user object (should include username/role).
#   - Optionally pass 'details' (dict or string) for extra context.
#
#  Author: Reginald
#  Last updated: 18th June 2025
#  =============================================================================

import datetime

def audit_log(action, user, details=None):
    """
    Write a structured audit log entry to both stdout and an audit log file.

    Args:
        action (str): The type of action/event (e.g., "login", "remediation_applied").
        user (dict): Dictionary with at least "username" and "role" keys.
        details (Any): Extra context or data about the event (optional).

    Output Example (stdout and file):
        [AUDIT] {
            "timestamp": "2024-06-21T13:45:12.345678",
            "user": "Reginald",
            "role": "admin",
            "action": "login",
            "details": {"ip": "127.0.0.1"}
        }
    """
    now = datetime.datetime.now().isoformat()
    entry = {
        "timestamp": now,
        "user": user["username"],
        "role": user["role"],
        "action": action,
        "details": details
    }
    # Print to terminal/log aggregator
    print("[AUDIT]", entry)
    # Also append to a persistent file for forensics/regulatory review
    with open("audit.log", "a") as f:
        f.write(str(entry) + "\n")

# =============================================================================
#  End of audit.py
# =============================================================================
