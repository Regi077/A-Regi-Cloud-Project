# Cloud Compliance Tool — Phase 8: Dashboard Backend

**Author:** Reginald

---

## 🚀 Overview

The **Dashboard Backend** (Phase 8) is the real-time, event-driven hub of the Cloud Compliance Tool. This microservice collects, aggregates, and streams live pipeline status updates from all backend compliance agents—empowering the UI and stakeholders with instant operational visibility. It leverages Flask, Flask-SocketIO, and RabbitMQ to provide scalable, zero-latency monitoring for every phase of the compliance lifecycle.

---

## 🎯 What Was Achieved 

- **Real-time aggregation and broadcasting** of compliance pipeline events (across all microservices) to UI clients.
- **WebSocket API** for seamless, low-latency delivery of live status updates to the frontend.
- **Modular topic monitoring**—add new pipelines or compliance stages without refactoring.
- **Threaded event consumers** ensure continuous and non-blocking event processing for each pipeline.
- **Centralized dashboard logic** to unify all compliance pipeline feedback in a single channel.
- **Onboarding-friendly, production-ready Docker deployment.**

---

## 🧑‍💻 Technology Stack

- **Python 3.13** (runtime)
- **Flask** (microservice framework)
- **Flask-SocketIO** (real-time WebSocket API)
- **Eventlet** (async server support for Socket.IO)
- **Pika** (RabbitMQ client library)
- **RabbitMQ** (event bus, handled externally)
- **Docker** (containerization)

---

## ✅ Phase 8 Functional Checklist

- [x] **RabbitMQ Topic Listener:** Consumes and processes events from all compliance pipeline topics (`rule.ingestion`, `validation.pipeline`, `remediation.pipeline`, `iam.pipeline`, `delta.pipeline`).
- [x] **WebSocket (Socket.IO) Gateway:** Pushes `pipeline_update` events to all connected frontend clients, instantly reflecting backend status changes.
- [x] **Dedicated Topic Threads:** Runs a background thread per pipeline, ensuring events are captured and relayed without blocking.
- [x] **Frontend-Ready API:** Serves as the central bridge for PipelineStatus and live dashboard panels in the UI.
- [x] **CORS Security:** Enables secure, cross-origin resource sharing for authorized frontends.
- [x] **Simple Extensibility:** Add or remove monitored pipelines by editing a single configuration list.
- [x] **Dockerized Delivery:** Fully containerized for one-command builds and effortless DevOps integration.

---

## 💡 How to Run

1. **Install dependencies:**  
   `pip install -r requirements.txt`
2. **Run the dashboard backend:**  
   `python app.py`
3. **Or use Docker Compose** (recommended for multi-pipeline stacks):  
   `docker compose up --build`
4. **Access the Dashboard Backend:**  
   - The backend will be available on port `5001` (mapped to container port `5000`).
   - Connect via WebSocket at `ws://localhost:5001` for live events.

---

📁 Project Structure (Highlights)

cloud-compliance-dashboard/
│
├── app.py              **Main Flask + Socket.IO event server**
├── event_bus.py        **RabbitMQ event consumer/utility**
├── requirements.txt    **# Python dependencies**
├── Dockerfile          **# Container build**

## 🚀 Closing

This phase delivers a single source of truth for all pipeline operations—enabling instant, interactive dashboard updates for compliance, engineering, and management users.

---