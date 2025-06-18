# =============================================================================
#  rules_engine.py  --  Pydantic-Based Compliance Rules Model & Rule Checker
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Defines the data model for compliance rules using Pydantic for validation.
#    - Implements a simple rule checker for evaluating if an IaC document satisfies a rule.
#
#  HOW TO EXTEND:
#    - Add new fields to ComplianceRule if your rules require more metadata.
#    - Replace or extend the `check_rule` function for smarter parsing/logic (e.g., regex, YAML/Terraform parsing).
# =============================================================================

from pydantic import BaseModel, ValidationError

# -------------------------------------------------------------------------
# ComplianceRule: Schema for all compliance rules.
# Each rule should have an ID, a descriptive name, the requirement text,
# the expected resource type (e.g., S3 Bucket, IAM Policy), the check condition,
# and the framework it belongs to (e.g., NIST 800-53, PCI-DSS, etc.).
# -------------------------------------------------------------------------
class ComplianceRule(BaseModel):
    id: int
    name: str
    requirement: str
    resource_type: str
    condition: str
    framework: str

# -------------------------------------------------------------------------
# check_rule: Very basic (dummy) rule evaluation logic.
# In a real system, you'd parse the IaC YAML/Terraform and check for compliance.
# For now, this simply checks if the rule's requirement text is present in the IaC code.
#
# Args:
#   iac_content (str): The uploaded Infrastructure-as-Code as a string.
#   rule (ComplianceRule): The rule object to check against.
# Returns:
#   bool: True if the requirement is found in IaC, else False.
# -------------------------------------------------------------------------
def check_rule(iac_content, rule):
    if rule.requirement.lower() in iac_content.lower():
        return True
    return False

# =============================================================================
#  End of rules_engine.py (Rule data model + basic checker)
# =============================================================================
