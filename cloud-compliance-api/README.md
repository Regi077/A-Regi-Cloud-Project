# Cloud Compliance Tool – Phase 2: API Gateway / MCP Layer

**Author:** Reginald 

---

## 🚀 Overview

This service forms the secure, audit-ready core of the cloud compliance pipeline. The **API Gateway / MCP Layer** acts as the main entry point for all user, compliance, and system operations. It features robust user authentication, role-based access control (RBAC), regulatory-grade auditing, and real-time observability. Every critical API action is traceable and securely logged, making this gateway the foundation for trustworthy compliance automation.

---

## 🎯 What Was Achieved

### 1. User Authentication & Role-Based Access
- **Secure login/logout endpoints** with credential validation.
- **RBAC enforced**: Only authorized roles can upload, scan, or submit logs.
- **Modular authentication** (pluggable `auth.py`, `rbac.py`) for easy updates.

### 2. Rich API Suite
- **/upload-doc** – Upload compliance documents (Admin/Service Provider only).
- **/get-frameworks** – List all supported frameworks (All users).
- **/start-scan** – Trigger a compliance scan (Admin/Service Provider only).
- **/submit-logs** – Submit log data (Admin/Service Provider only).

### 3. Auditing, Observability & Security
- **Comprehensive audit logging**: All sensitive actions are tracked (who, when, what).
- **Regulatory-grade endpoint audit**: Select endpoints produce granular audit trails.
- **Real-time event publishing**: User and security events published to RabbitMQ.
- **Rate limiting**: Defends against brute-force and API abuse.
- **Global error handler**: Captures and reports all exceptions for security analysis.
- **CORS policy**: Secure cross-origin resource sharing for frontend/backend safety.

### 4. Regulatory & Compliance-Ready
- **Selective endpoint auditing** for all regulatory and security-sensitive APIs.
- **Audit event publishing** to RabbitMQ (`audit.log`, `user.activity`, `security.alert`, etc.).
- **Rotating `audit.log` file** for forensic and regulatory evidence.

### 5. Modern Cloud-Native Architecture
- **Dockerized service**: Clean, production-ready Dockerfile.
- **Stateless, 12-factor structure**: Easy to deploy, scale, and extend.
- **Blueprint modularization**: Endpoints separated for clear onboarding and future upgrades.

---

## 🛠️ Technology Stack

- **Python 3.13** – Primary language and runtime
- **Flask** – Web framework (API endpoint management)
- **Flask-Limiter** – API rate limiting
- **Flask-CORS** – Secure cross-origin handling
- **RabbitMQ** – Event bus for audit/security events
- **pika** – Python/RabbitMQ integration
- **Docker** – Containerization for microservice deployment

---

## ✅ Phase 2 Functionality Checklist

- [x] **Credential-Based Login/Logout**
- [x] **Role-Based Access Control (Admin / Service Provider / Client)**
- [x] **Document Upload API (RBAC-restricted)**
- [x] **Framework Listing API (Open to all authenticated users)**
- [x] **Scan Initiation API (RBAC-restricted)**
- [x] **Log Submission API (RBAC-restricted)**
- [x] **Comprehensive Audit Logging to File**
- [x] **Security Event Publishing (RabbitMQ)**
- [x] **Rate Limiting (Abuse Prevention)**
- [x] **CORS Configuration**
- [x] **Global Error Handling & Security Alerts**
- [x] **Fine-Grained Regulatory Endpoint Audit**
- [x] **Dockerized for Container Environments**
- [x] **Modular, Blueprint-Driven Codebase**
- [x] **Rich Inline Comments for Easy Onboarding**

---

## 📁 Directory Structure (Key Files)
cloud-compliance-api/
├── app.py # Main Flask application (API + RBAC + audit)
├── endpoints.py # All business logic endpoints (upload, scan, logs, etc.)
├── auth.py # Authentication logic
├── rbac.py # Role-based access control
├── audit.py # File/system audit logging
├── event_bus.py # Publishes events to RabbitMQ
├── users.json # Example user/role store
├── requirements.txt # Python dependencies
├── Dockerfile # Container build instructions

##  How to Run (Development & Docker)

**Locally (with Python)**

pip install -r requirements.txt
python app.py

---

## 🚀 Closing

This API Gateway is the security and compliance heart of the Cloud Compliance platform.
Every operation is RBAC-checked, fully audited, and observable in real time.
Ready for zero-trust environments, high-stakes audits, and rapid integration into advanced compliance pipelines.

---