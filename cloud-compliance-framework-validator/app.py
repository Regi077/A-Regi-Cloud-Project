from flask import Flask, request, jsonify
from flask_cors import CORS
from qdrant_utils import get_rules_from_qdrant  # FIXED: import from qdrant_utils
from validation_utils import validate_iac_against_rules

UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/validate-framework', methods=['POST'])
def validate_framework():
    # 1. Receive IaC (YAML or Terraform block as text) and framework name
    iac_file = request.files["iac"]
    iac_content = iac_file.read().decode("utf-8")
    framework = request.form["framework"]

    # 2. Load rules from Qdrant
    rules = get_rules_from_qdrant(framework)

    # 3. Validate IaC against rules
    validation_result = validate_iac_against_rules(iac_content, rules)

    return jsonify(validation_result)

if __name__ == "__main__":
    app.run(port=5020, debug=True)
