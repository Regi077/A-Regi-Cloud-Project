from rules_engine import ComplianceRule, check_rule

def validate_iac_against_rules(iac_content, rules):
    passed = []
    failed = []
    recommendations = []

    for idx, r in enumerate(rules):
        try:
            rule = ComplianceRule(**r)
        except Exception:
            continue  # Skip if schema invalid

        if check_rule(iac_content, rule):
            passed.append(rule.name)
        else:
            failed.append(rule.name)
            # Recommendation: template string based on rule (dummy for now)
            recommendations.append({
                "rule": rule.name,
                "suggested_fix": f"Add {rule.requirement} to resource {rule.resource_type}."
            })

    return {
        "passed": passed,
        "failed": failed,
        "recommendations": recommendations
    }
