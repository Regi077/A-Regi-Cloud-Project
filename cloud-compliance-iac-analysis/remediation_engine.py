# =============================================================================
#  remediation_engine.py -- Automated IaC Compliance Analysis & Remediation
# =============================================================================
#  Author: Reginald 
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - This module analyzes Infrastructure-as-Code (IaC) files for compliance
#      with key cloud security controls.
#    - It identifies missing controls and generates remediation suggestions
#      as ready-to-use Terraform/YAML blocks for the user.
#
#  USAGE:
#    - Import and call analyze_and_remediate(iac_content, framework)
#      in your Flask endpoint after receiving IaC text from the user.
#
#  HOW TO EXTEND:
#    - To support new frameworks, expand `required_controls` below or make
#      it dynamically load controls by framework name.
#    - Add more controls as you refine your compliance baseline.
# =============================================================================

def analyze_and_remediate(iac_content, framework):
    """
    Analyze the given IaC content against a set of required controls.
    If a control is missing, suggest a remediation block.
    Returns a dict of failed controls and suggestions.
    
    Args:
        iac_content (str): The raw contents of the user's IaC file.
        framework (str): Name of the compliance framework (not used here, but kept for future extension).
    Returns:
        dict: { "failed": [...], "suggestions": [...] }
    """
    # -------------------------------------------------------------------------
    # Compliance Controls Baseline (Azure-focused, expand as needed)
    # Each item has:
    #   - id: Unique control ID
    #   - rule: Plain English description
    #   - check: String to search for in IaC
    #   - suggestion: Remediation Terraform/YAML snippet
    # -------------------------------------------------------------------------
    required_controls = [
        {
            "id": 1,
            "rule": "Enable soft delete for Blob Storage",
            "check": "soft_delete_retention_policy",
            "suggestion": (
                'resource "azurerm_storage_account" "example" {\n'
                '  ...\n'
                '  blob_properties {\n'
                '    delete_retention_policy {\n'
                '      days = 7\n'
                '    }\n'
                '  }\n'
                '}'
            )
        },
        {
            "id": 2,
            "rule": "Enforce HTTPS traffic only on Storage Account",
            "check": "enable_https_traffic_only",
            "suggestion": 'enable_https_traffic_only = true'
        },
        {
            "id": 3,
            "rule": "Enable Storage Account encryption",
            "check": "encryption",
            "suggestion": (
                'encryption {\n'
                '  services {\n'
                '    blob {\n'
                '      enabled = true\n'
                '    }\n'
                '    file {\n'
                '      enabled = true\n'
                '    }\n'
                '  }\n'
                '  key_type = "Account"\n'
                '}'
            )
        },
        {
            "id": 4,
            "rule": "Restrict network access with firewall rules",
            "check": "network_rules",
            "suggestion": (
                'network_rules {\n'
                '  default_action             = "Deny"\n'
                '  bypass                    = ["AzureServices"]\n'
                '  ip_rules                  = ["YOUR.IP.HERE.1", "YOUR.IP.HERE.2"]\n'
                '}'
            )
        },
        {
            "id": 5,
            "rule": "Enable advanced threat protection",
            "check": "advanced_threat_protection",
            "suggestion": (
                'resource "azurerm_advanced_threat_protection" "example" {\n'
                '  target_resource_id = azurerm_storage_account.example.id\n'
                '  enabled            = true\n'
                '}'
            )
        }
    ]

    failed = []      # List of controls that are missing in the IaC
    suggestions = [] # Remediation blocks for any failed controls

    for control in required_controls:
        # Check if each control is already present in the user's IaC file.
        if control["check"] not in iac_content:
            failed.append(control["rule"])
            suggestions.append({
                "id": control["id"],
                "text": control["rule"],
                "priority": "High",  # All are critical for demo—can customize per control
                "suggested_block": control["suggestion"]
            })

    return {
        "failed": failed,
        "suggestions": suggestions
    }

# =============================================================================
#  End of remediation_engine.py (Plug into /analyze-iac API endpoint)
# =============================================================================
