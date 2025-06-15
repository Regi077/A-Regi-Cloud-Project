import datetime

def audit_log(action, user, details=None):
    now = datetime.datetime.now().isoformat()
    entry = {
        "timestamp": now,
        "user": user["username"],
        "role": user["role"],
        "action": action,
        "details": details
    }
    # Log to stdout
    print("[AUDIT]", entry)
    # Optionally, also log to file
    with open("audit.log", "a") as f:
        f.write(str(entry) + "\n")
