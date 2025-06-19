# Cloud Compliance Tool – Phase 4: Framework Validation Pipeline

---
**Author:** Reginald 

---

## 🚀 Overview

**Phase 4: Framework Validation Pipeline** delivers automated, auditable, and intelligent compliance validation for Infrastructure-as-Code (IaC) against industry and regulatory security frameworks. This microservice receives IaC definitions, fetches the relevant rules from the Qdrant vector database, and runs deep validation, providing both granular compliance results and actionable remediation recommendations. Designed for secure, cloud-native deployments and real-time dashboard integration, it is the heart of proactive, audit-ready cloud security assurance.

---

## 🎯 What Was Achieved 

- **Automated Validation of IaC Against Compliance Frameworks:**  
  Dynamically analyzes user-uploaded IaC files against a chosen security framework, producing detailed pass/fail results and executive-ready recommendations.

- **Seamless Integration with Rule Database (Qdrant):**  
  Instantly retrieves and applies framework-specific rules using scalable, vectorized queries from the Qdrant DB.

- **Real-Time Audit and Observability:**  
  Publishes validation events to RabbitMQ, supporting live dashboard updates and executive oversight.

- **Remediation Guidance:**  
  For every failed compliance rule, generates step-by-step recommendations for fast, foolproof remediation.

- **Idiot-Proof, Secure API Endpoints:**  
  All endpoints are CORS-enabled, fully documented, and robust against malformed input or attack attempts.

---

## 🧑‍💻 Technology Stack

- **Python 3.13** — Core application logic and validation flows
- **Flask** + **Flask-CORS** — Secure, idiot-proof API endpoints
- **Pydantic** — Reliable data validation and rule modeling
- **Qdrant Vector Database** — High-performance, framework rule storage and retrieval
- **RabbitMQ** — Event-driven architecture for live observability and alerting
- **Docker** — Containerized, reproducible, and cloud-native deployments

---

## Phase 4 Functional Checklist

- [x] Accept and parse user-submitted IaC files (YAML, Terraform, plain text).
- [x] Allow user to select desired compliance framework (NIST, PCI, HIPAA, GDPR, etc.).
- [x] Retrieve matching rules for the selected framework from Qdrant.
- [x] Validate each IaC resource against all framework rules using robust schema checks.
- [x] Generate a granular validation report:  
    - **Passed** and **Failed** checks for each rule.
    - Actionable, context-specific remediation advice.
- [x] Publish a summary event (`validation.pipeline`) to RabbitMQ for dashboard and audit integration.
- [x] Fully Dockerized, CORS-protected, and designed for secure cloud-native deployment.
- [x] Clear, developer-friendly error handling and onboarding documentation.

---

## How to Run

1. **Build & Start the Service (via Docker Compose):**
    ```bash
    docker compose up --build framework-validation
    ```
2. **API Endpoint:**  
   POST your IaC file and chosen framework to:
   Form fields:
- `iac`: (file) Your IaC YAML/TF/text file.
- `framework`: (string) Framework name (e.g., "NIST", "PCI", "GDPR").

3. **Live Validation Results:**  
All validation results are published in real-time to the dashboard via RabbitMQ (`validation.pipeline` topic).

---


   ## Folder Structure

cloud-compliance-framework-validator/
│
├── app.py # Main Flask application
├── event_bus.py # Publishes validation events to RabbitMQ
├── qdrant_utils.py # Rule retrieval from Qdrant DB
├── validation_utils.py # Validation logic and remediation generation
├── rules_engine.py # Pydantic compliance rule models
├── requirements.txt # Python dependencies
├── Dockerfile # Container build
├── uploads/ # (auto-created) For file uploads
└── venv/ # (ignored) Python virtual environment


---
*## 🚀 Closing

**This service is production-ready for integration with cloud security operations and executive dashboards. For technical help, see code comments or contact Reginald/Team.**
Every compliance validation is fully logged and pushed to the event bus for traceability.

---