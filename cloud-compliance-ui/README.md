# Cloud Compliance Tool — Phase 1: Frontend UI (React)

**Author:** Reginald / Team  
**Last Updated:** 18th June 2025

---

## 🚀 Overview

This repository contains the **Frontend UI** for the Cloud Compliance Tool—a modern, dashboard that enables organizations to manage, visualize, and interact with their cloud compliance lifecycle.

**Phase 1** focused on delivering a robust, real-time, and user-friendly React application that integrates seamlessly with all backend compliance microservices. The UI is role-aware, and designed for rapid onboarding of both engineers and compliance teams.

---

## 🎯 What Was Achieved (Executive Summary)

- **Role-based Dashboard:**  
  Delivered a fully responsive, role-driven UI that dynamically presents functionality based on user type (Admin, Service Provider, Client).

- **Integrated Compliance Workflows:**  
  Supports framework upload, architecture/IaC validation, automated remediation suggestions, IAM auditing, delta analysis, and live agent status—all accessible via intuitive panels.

- **Real-Time Observability:**  
  Live pipeline/agent status updates powered by Socket.IO, giving instant feedback on the progress of backend compliance pipelines.

- **Idiot-Proof Onboarding:**  
  All interactions are designed to be frictionless. Detailed in-app labels, error handling, and clear user feedback make this UI accessible even for non-technical stakeholders.

- **Executive-Ready Foundation:**  
  Built with extensibility, auditability, and maintainability at the forefront—ensuring rapid scaling in later phases.

---

## 🧑‍💻 Technology Stack

- **React 19 + Vite** (Front-end framework, lightning-fast dev/build tooling)
- **Tailwind CSS** (Utility-first CSS framework for modern UI)
- **Socket.IO Client** (Real-time pipeline status/notifications)
- **Docker** (Multi-stage build for reproducible deployments)
- **RBAC Logic** (Enforced on the frontend for panel/tab access)
- **ESLint** (Consistent code quality and best practices)
- **Modern JavaScript** (ES2023+, hooks, async/await)
- **Full support for API integrations:** All panels interact with Python/Flask backend microservices

---

## ✅ Phase 1 Functional Checklist

### 1. Project Foundation
- [x] **React + Vite Setup:** Clean structure, fast builds, scalable foundation.
- [x] **TailwindCSS Integrated:** Consistent, elegant UI.
- [x] **Socket.IO Client:** Real-time pipeline updates.

### 2. Core UI Panels/Components
- [x] **Login Page:** Clean, role-aware authentication.
- [x] **Dashboard:** Dynamic navigation, user-aware panels.

### 3. Main Functional Panels
- [x] **Framework Upload:** Upload compliance docs to backend.
- [x] **Architecture Input:** Paste/upload IaC for validation.
- [x] **Engineering Panel:** See, accept, and download remediation suggestions.
- [x] **IAM Audit Panel:** Audit IAM policies for security risks.

### 4. Advanced Features
- [x] **Pipeline Status Panel:** Real-time agent status.
- [x] **Delta Analysis Panel:** Pre/post compliance change analysis, PDF export.
- [x] **Agent Reasoning Panel:** See agent decision trace.
- [x] **Risk Diagram:** Placeholder for risk visualizations.

### 5. Usability, Security, and Robustness
- [x] **RBAC Enforcement:** Tabs/panels by role.
- [x] **Form Validation & Error Handling:** Everywhere.
- [x] **Responsive, Accessible UI:** Looks great everywhere.
- [x] **Rich Inline Documentation:** Developer- and onboarding-friendly.

### 6. DevOps/Containerization
- [x] **Production Dockerfile:** Multi-stage, Vite preview for development/testing.
- [x] **Docker Compose Integration:** One command for full stack.

### 7. Knowledge Transfer & Maintenance
- [x] **Source/Config Files Included:**  
  - `package.json`, `tailwind.config.cjs`, `postcss.config.cjs`, `vite.config.cjs`
- [x] **Demo User Data:**  
  - (`rbac.js`) for frictionless onboarding/testing.

---

## 💡 How to Run (Development & Docker)

**Locally (with Node):**
```bash
npm install
npm run dev         # or: npm run build && npm run preview
