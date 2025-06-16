from pydantic import BaseModel, ValidationError

class ComplianceRule(BaseModel):
    id: int
    name: str
    requirement: str
    resource_type: str
    condition: str
    framework: str

def check_rule(iac_content, rule):
    # Dummy implementation; in reality, this would parse and evaluate
    # For this template, just check if 'requirement' string is present in IaC
    if rule.requirement.lower() in iac_content.lower():
        return True
    return False
