# This code is part of the cloud-compliance-iac-analysis project.
# It is designed to analyze Infrastructure as Code (IaC) files  
# against compliance frameworks and provide remediation suggestions.
# The application uses Flask for the web framework and Flask-CORS for handling CORS.    

from flask import Flask, request, jsonify
from flask_cors import CORS
from remediation_engine import analyze_and_remediate

UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/analyze-iac', methods=['POST'])
def analyze_iac():
    iac_file = request.files["iac"]
    framework = request.form["framework"]
    iac_content = iac_file.read().decode("utf-8")

    analysis = analyze_and_remediate(iac_content, framework)
    return jsonify(analysis)

if __name__ == "__main__":
    app.run(port=5030, debug=True)


