# Cloud Compliance Tool – Phase 5: IaC Analysis Pipeline

**Author:** Reginald 
---

## 🚀 Overview

This repository introduces an intelligent, automated pipeline for analyzing Infrastructure-as-Code (IaC) against security and compliance standards. This module enables rapid, error-proof detection of misconfigurations and provides immediate, actionable remediation recommendations—empowering DevOps and security teams to fix issues before deployment.

---

## 🎯 What Was Achieved 

- **End-to-End IaC Analysis:** Accepts user-uploaded YAML, Terraform, or text files and parses them for compliance checks.

- **Framework-Specific Assessment:** Allows the user or system to select a relevant compliance framework (e.g., Azure, NIST, AWS), ensuring context-aware evaluation.

- **Automated Compliance Validation:** Checks for critical configuration controls (e.g., encryption, soft delete, firewall rules) and flags failures.

- **Remediation Recommendation Engine:** Instantly generates tailored, copy-paste remediation blocks for every failed control, annotated by risk priority.

- **Event-Driven Updates:** Publishes analysis outcomes to RabbitMQ, powering real-time dashboard visualizations and traceability.

- **API-First Integration:** Exposes a developer-friendly endpoint for easy automation, CI/CD integration, or UI consumption.

- **Cloud-Native and Secure:** Fully containerized, CORS-enabled, and robust against malformed inputs, making it suitable for production cloud environments.

---

## 🧑‍💻 Technology Stack

- **Python 3.13** – Main application language
- **Flask** – API framework for web service
- **Flask-CORS** – Secure cross-origin requests
- **pydantic** – Data validation and parsing
- **requests** – HTTP client for internal/external calls
- **ruamel.yaml** – YAML file parsing
- **RabbitMQ** – Event bus for real-time communication
- **Docker** – Containerization for easy deployment

---

## ✅ Phase 5 Functional Checklist

- **IaC File Ingestion and Parsing**
  - Accepts user-submitted IaC files (YAML, Terraform, plain text) via API.
  - Parses uploaded files and safely reads relevant content.

- **Framework-Aware Analysis**
  - Supports compliance framework selection (Azure, AWS, NIST, etc.).
  - Compares IaC against required compliance controls.

- **Automated Compliance Checks**
  - Scans for key configuration patterns directly in IaC.
  - Flags missing or misconfigured controls as compliance failures.

- **Remediation Suggestions**
  - Generates copy-paste remediation code for each failure.
  - Annotates suggestions with priority and human-readable guidance.

- **Event-Driven Architecture**
  - Publishes results (failed checks, remediation) to RabbitMQ for live dashboard updates.

- **Developer-Friendly API**
  - POST endpoint `/analyze-iac` returns structured JSON results.

- **Resilient & Cloud-Ready**
  - Robust error handling for invalid files/inputs.
  - Containerized for scalable, cloud-native deployment.

- **Traceability and Security**
  - All runs are tracked for audit; CORS-enabled endpoints.

---

## How to Run

1. **Build the Docker image**  
   ```sh
   docker build -t iac-analysis .


2. **Start the container**
docker run -p 5030:5030 --network your-docker-network iac-analysis


## 🚀 Closing

Phase 5 empowers organizations with proactive, real-time IaC compliance checks and “one-click” remediation. By combining automated analysis, instant actionable advice, and event-driven integration, this pipeline closes the compliance gap—helping security, engineering, and cloud teams deliver secure infrastructure at speed.

---