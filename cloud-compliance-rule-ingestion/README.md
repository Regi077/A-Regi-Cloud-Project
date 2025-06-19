# Cloud Compliance Tool – Phase 3: Rule Ingestion Pipeline

**Author:** Reginald

---

## Overview

Phase 3 of the Cloud Compliance Tool delivers an automated, AI-driven pipeline for ingesting compliance frameworks and extracting actionable rules. This microservice streamlines the transformation of raw PDF or text-based regulations into machine-readable JSON, seamlessly inserting them into a vector database (Qdrant) for downstream compliance validation and remediation.

## 🎯 What Was Achieved

- **End-to-End Automated Rule Ingestion:**  
  Successfully automated the upload, parsing, and AI-driven extraction of compliance rules from unstructured PDF and text documents, dramatically reducing manual labor and error-prone processes.

- **Seamless Integration with Vector Database:**  
  Extracted rules are structured, serialized as JSON, and upserted into a scalable Qdrant vector database for fast, intelligent search and downstream compliance validation.

- **Event-Driven, Observable Architecture:**  
  Every ingestion triggers real-time event publishing via RabbitMQ, supporting live dashboards and enabling orchestration across all pipeline phases.

- **Modular, Cloud-Native Service:**  
  The entire rule ingestion flow is fully containerized, cloud-agnostic, and built with extensibility and security as first-class priorities.
  
- **Executive & Audit-Friendly:**  
  Achieves full traceability from document upload to actionable compliance rules, with robust error handling, reporting, and isolation.

---

## 🧑‍💻 Technology Stack

- **Python 3.13** – Primary programming language.
- **Flask** – Web server and API framework.
- **Flask-CORS** – CORS support for frontend-backend integration.
- **PyPDF2** – PDF text extraction.
- **Requests** – HTTP client for LLM integration.
- **Qdrant-Client** – Vector database interaction (for rules storage/search).
- **Ollama** – Local LLM service for compliance rule extraction.
- **Pika** – RabbitMQ event bus integration for real-time updates.
- **Docker** – Containerization for cloud-native, reproducible builds.

---

## Phase 3 – Functional Checklist

- [x] **File Upload Handling**
  - Securely accepts and stores compliance frameworks (PDF/TXT).
- [x] **Document Parsing & Chunking**
  - Efficiently reads and splits documents, prepares for LLM extraction.
- [x] **AI-Driven Rule Extraction**
  - Integrates with Ollama LLM to convert raw regulations into JSON rule objects.
  - Robust prompt design, error handling, and extraction recovery.
- [x] **JSON Serialization**
  - Stores all extracted rules in versioned, human-readable JSON files.
- [x] **Vector Database Upsert**
  - Inserts rules into Qdrant with auto-collection creation and placeholder embeddings.
- [x] **Multi-Tenancy & Tagging**
  - Supports rules tagged by compliance framework and fallback for incomplete metadata.
- [x] **Event-Driven Pipeline**
  - Publishes every successful ingestion to RabbitMQ (`rule.ingestion` topic) for live dashboard/status monitoring.
- [x] **Cloud-Native, DevOps-Ready**
  - Isolated in a production-grade Docker container.
  - Modular utilities for parsing, extraction, and DB interaction.
- [x] **Security & Validation**
  - Validates upload types, handles unsafe content, and recovers from LLM/database errors.

---

## Quick Start

1. **Build and run using Docker Compose** (see project root):
    ```bash
    docker compose up --build rule-ingestion
    ```
2. **Upload a framework document**  
   POST a `.pdf` or `.txt` file to:
    ```
    POST http://localhost:5010/ingest-doc
    Form-data: file=[your_file.pdf or .txt]
    ```
3. **Observe Events**  
   Successful ingestion triggers event publishing to RabbitMQ (`rule.ingestion`).

---

## Project Structure
cloud-compliance-rule-ingestion/
├── app.py # Main API server
├── event_bus.py # Event publishing to RabbitMQ
├── ollama_client.py # LLM interaction for rule extraction
├── parse_utils.py # PDF/text parsing, chunking, extraction, save JSON
├── qdrant_utils.py # Qdrant upsert logic
├── requirements.txt # Python dependencies
├── Dockerfile # Container build
├── uploads/ # Uploaded frameworks
├── parsed_rules/ # JSON-extracted rules
└── venv/ # (Local Python virtual environment)

---

## How It Works

1. **Upload**: User submits a PDF or TXT regulation document.
2. **Parse & Chunk**: Document is split into processable chunks.
3. **Extract**: Each chunk is passed to Ollama LLM for rule extraction.
4. **Serialize**: All rules are aggregated and saved as JSON.
5. **Upsert**: Rules are pushed into Qdrant for searchable, scalable compliance validation.
6. **Publish**: Event is published to RabbitMQ for system-wide observability and automation.

---

## Extensibility

- Easily plug in new LLM models or prompt templates.
- Add new document formats by extending `parse_utils.py`.
- Integrate with further downstream pipelines (validation, remediation) via event bus.

---

## Security & Compliance

- Secure file handling and upload validation.
- Isolated Docker environment—no host file leaks.
- Designed for cloud or on-prem deployment, audit-friendly.

---

*## 🚀 Closing

It uses the Phase 1 template as a standard, integrates your detailed checklist, and clearly communicates the technology stack and key achievements to audiences.

---