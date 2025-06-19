# Cloud Compliance Tool — Phase 7: Delta Analysis Pipeline

**Author:** Reginald  

## 🚀 Overview

The **Delta Analysis Pipeline** is designed to provide rapid, field-level compliance comparison between infrastructure states before and after remediation. This microservice automates the detection and reporting of changes, calculates pass/fail rates, and generates auditable PDF reports to accelerate compliance review, audit response, and operational transparency.

---

## 🎯 What Was Achieved

- Automated delta (change) analysis between **pre-remediation** and **post-remediation** JSON states.

- Pass/fail evaluation and scoring across all fields, supporting executive-level insight.

- One-click PDF export for evidence-ready compliance reporting.

- Real-time event publishing to RabbitMQ, enabling live dashboard integration.

- Secure, modular, and fully containerized microservice suitable for enterprise and multi-cloud deployments.

---

## 🧑‍💻 Technology Stack

- **Language:** Python 3.13
- **Frameworks:** Flask, Flask-CORS
- **Document Generation:** ReportLab
- **Event Bus:** RabbitMQ (via `pika` Python library)
- **Containerization:** Docker
- **API:** REST (JSON in/out), CORS-enabled
- **Dashboard Integration:** WebSocket/event-driven updates

---

## ✅ Phase 7 Functional Checklist

- **Delta Analysis Automation**
  - Accepts two JSON objects (“pre-remediation” and “post-remediation”) via secure REST API.
  - Automatically computes field-by-field differences, highlighting all compliance-relevant changes.
  - Clearly classifies each field as **Passed** (no change) or **Failed** (altered after remediation).

- **Pass/Fail Scoring & Reporting**
  - Calculates and returns a **Pass Percentage** (% of fields that are unchanged).
  - Produces a structured report, listing all passed/failed fields and summarizing changes with “before” and “after” values.

- **PDF Report Generation**
  - Generates an executive-grade, downloadable PDF documenting the delta analysis and key compliance changes.
  - Ensures full audit traceability for external and internal stakeholders.

- **Event-Driven Dashboard Integration**
  - Publishes each delta analysis event to RabbitMQ (`delta.pipeline` topic).
  - Enables real-time dashboard updates for CISO, security, and compliance teams.

- **Robust, Hassle-Free REST API**
  - **POST `/compare`:** Receives `{ pre: <json>, post: <json> }`, returns delta results, pass %, and all change details.
  - **POST `/export`:** Accepts delta result, returns a PDF report.

- **Developer & Audit Friendly**
  - Human-readable, modular, and well-documented codebase.
  - Clear error handling for input validation and JSON parsing.
  - PDF exports are persisted in a dedicated volume for long-term record keeping.

- **Cloud-Native & Secure**
  - Fully containerized with Docker; designed for modern, multi-cloud environments.
  - CORS-enabled and seamlessly integrates with the compliance dashboard UI.

---

## How It Works

1. **Submit**: Send “pre” and “post” compliance state JSONs to the `/compare` endpoint.
2. **Analyze**: The pipeline computes and returns a full delta analysis—field-by-field results, pass/fail breakdown, and summary.
3. **Export**: Generate a PDF report with a single API call (`/export`), providing clear evidence of compliance improvements.
4. **Track**: Every analysis event is published to RabbitMQ, supporting real-time dashboard monitoring.
5. **Persist**: All PDF reports are saved to the host machine for robust, auditable record keeping.

---

## Usage

- **Run as Docker container** (from the project root):
  ```bash
  docker compose up --build delta-analysis


`📁 Project Structure (Highlights)`

`cloud-compliance-delta-analysis/`
`├── app.py`
`├── delta_utils.py`
`├── event_bus.py`
`├── requirements.txt`
`├── Dockerfile`
`├── reports/                  # All exported PDF reports are saved here`


## 🚀 Closing

Here Delta analysis moves compliance from a checkbox exercise to an auditable, data-driven practice. This pipeline arms your team with real, defensible evidence for every remediation effort—instantly ready for executives, auditors, or regulators.

---
