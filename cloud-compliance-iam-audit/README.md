# Cloud Compliance Tool — Phase 6: IAM Audit Pipeline

> **Author:** Reginald 

---

## 🚀 Overview

The **IAM Audit Pipeline** is a dedicated microservice within the Cloud Compliance suite that automates the detection of security risks, privilege escalations, and policy misconfigurations across your cloud IAM landscape. This phase is designed to offer actionable, real-time insights on user and group permissions, enforcing least privilege and ensuring compliance with internal and external security mandates.

---

## 🎯 What Was Achieved 

- **Automated IAM Risk Detection:**  
  - Root user without MFA (flagged as high risk).
  - Overprivileged users/groups (e.g., "admin" or wildcard `*` permissions).
  - Excessive permission sets (>10), indicating least-privilege violations.
  - Group-level “full_access” policy detection.

- **Structured Risk Categorization:**  
  - Risks are aggregated into high, medium, and low categories.
  - Detailed explanations accompany each finding for transparency and auditability.

- **Flexible Input & User Experience:**  
  - Accepts IAM configuration via file upload or direct JSON input.
  - Robust, onboarding-friendly REST API: `/audit-iam` (POST).

- **Real-Time Event Publishing:**  
  - Instantly emits audit summaries to RabbitMQ (`iam.pipeline` topic) for live dashboard updates.

- **Seamless Integration & Traceability:**  
  - Results are visualized in the compliance dashboard for central monitoring.
  - Color-coded outputs ready for risk visualization and executive review.

- **Cloud-Native, Secure, and Extensible:**  
  - Hardened against malformed input, easily extensible for new rules.
  - Runs containerized for hassle-free deployment and scaling.

---

## 🧑‍💻 Technology Stack

- **Python 3.13**
- **Flask** (REST API framework)
- **Flask-CORS** (Cross-Origin Resource Sharing)
- **pika** (RabbitMQ client for Python)
- **Docker** (Containerization)
- **RabbitMQ** (Event bus for real-time updates)

---

## ✅ Phase 5 Functional Checklist

- **IAM Policy & Access Review**
  - Accepts and audits user/group privileges and permissions (string/array).
  - Handles both direct file upload and manual JSON input.

- **Automated Security Risk Detection**
  - Detects root users lacking MFA (high risk).
  - Flags users/groups with “admin” privilege or `*` wildcard permissions.
  - Highlights users/groups with excessive permissions (>10).
  - Detects “full_access” policies on groups.

- **Risk Categorization & Scoring**
  - Aggregates findings into high, medium, and low risk.
  - Returns clear, structured results.

- **Event-Driven Observability**
  - Publishes audit results to RabbitMQ for live dashboard integration.

- **Developer-Friendly API**
  - `/audit-iam` (POST): Accepts JSON and returns risk assessment.

- **Cloud-Native & Traceable**
  - Fully containerized (Docker).
  - CORS-enabled and secure.

---


## 📦 Usage

1. **Run with Docker Compose**  
   This microservice is orchestrated as `iam-audit` in your project’s `docker-compose.yml`.

   ```bash
   docker compose up iam-audit

   Live Dashboard Integration:
   Results are published to RabbitMQ for real-time monitoring in the main dashboard.
