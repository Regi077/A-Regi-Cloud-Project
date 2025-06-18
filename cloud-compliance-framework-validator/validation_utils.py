# =============================================================================
#  validation_utils.py  --  IaC Validation Against Compliance Rules Engine
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Validates user-submitted Infrastructure-as-Code (IaC) text against a list of compliance rules.
#    - Uses Pydantic for schema validation and robust data handling.
#    - Outputs which rules passed, which failed, and remediation recommendations for any failures.
#
#  HOW TO EXTEND:
#    - Improve the `check_rule` logic for more advanced IaC parsing (YAML/Terraform).
#    - Refine or expand recommendations for failed rules.
#    - Integrate detailed error handling if your rule schema changes.
# =============================================================================

from rules_engine import ComplianceRule, check_rule

# -------------------------------------------------------------------------
# validate_iac_against_rules:
#   Given the content of an IaC file and a list of rule dicts,
#   checks each rule for compliance and returns summary results.
#
# Args:
#   iac_content (str): The raw IaC code (YAML/Terraform) as a string.
#   rules (list[dict]): List of compliance rule dicts, e.g. from Qdrant or elsewhere.
#
# Returns:
#   dict: {
#     "passed": List of rule names that were satisfied,
#     "failed": List of rule names that were not satisfied,
#     "recommendations": List of suggested remediation actions for failed rules
#   }
# -------------------------------------------------------------------------
def validate_iac_against_rules(iac_content, rules):
    passed = []
    failed = []
    recommendations = []

    for idx, r in enumerate(rules):
        try:
            # Use Pydantic to ensure the rule is valid and correctly structured
            rule = ComplianceRule(**r)
        except Exception:
            # Skip this rule if schema or data is invalid (defensive coding)
            continue

        if check_rule(iac_content, rule):
            passed.append(rule.name)
        else:
            failed.append(rule.name)
            # Add a recommendation for each failed rule (can be customized)
            recommendations.append({
                "rule": rule.name,
                "suggested_fix": f"Add {rule.requirement} to resource {rule.resource_type}."
            })

    return {
        "passed": passed,
        "failed": failed,
        "recommendations": recommendations
    }

# =============================================================================
#  End of validation_utils.py (IaC rule compliance logic)
# =============================================================================
