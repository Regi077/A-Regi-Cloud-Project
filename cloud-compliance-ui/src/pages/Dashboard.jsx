// =============================================================================
//  Dashboard.jsx -- Executive, Hassle-Free Compliance UI Main Panel
// =============================================================================
//  Author: Reginald
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Central dashboard with tabbed navigation for all compliance workflows.
//    - Role-based access control: panels/tabs rendered based on user.role.
//    - Integrates live status, remediation, upload, IAM, risk visualization, etc.
//    - Code and comments intentionally “idiot-proofed” for fast onboarding.
//
//  HOW TO EXTEND:
//    - To add a tab: update TABS, add render line below, adjust RBAC if needed.
//    - All panels are decoupled components for easy future swaps/reuse.
//    - Business logic for RBAC lives here, so never duplicate elsewhere.
// =============================================================================

import React, { useState } from "react";
import FrameworkUpload from "../components/FrameworkUpload.jsx";
import ArchitectureInput from "../components/ArchitectureInput.jsx";
import EngineeringPanel from "../components/EngineeringPanel.jsx";
import RiskDiagram from "../components/RiskDiagram.jsx";
import PipelineStatus from "../components/PipelineStatus.jsx"; // Live agent status (real-time, Socket.IO)
import AgentReasoning from "../components/AgentReasoning.jsx";
import IamAuditPanel from "../components/IamAuditPanel.jsx"; // IAM policy/risk audits
import DeltaAnalysisPanel from "../components/DeltaAnalysisPanel.jsx"; // Compliance delta reporting

// === Tab Definitions ===
// Each object describes a tab. Order = tab row order.
// Extend this array to add new tabs in the future.
const TABS = [
  { key: "status", label: "Pipeline Status" },      // Shows real-time status for all backend agents
  { key: "framework", label: "Frameworks" },        // Upload/view compliance frameworks
  { key: "arch", label: "Architecture" },           // Upload/view system/IaC architectures
  { key: "eng", label: "Engineering" },             // Remediation suggestions, accept/reject
  { key: "iam", label: "IAM Audit" },               // IAM role/policy audit panel
  { key: "risk", label: "Risk Diagram" },           // Visualization of risk/priorities
  { key: "reason", label: "Agent Reasoning" },      // Agent’s thought process & decision tree
  { key: "delta", label: "Delta Analysis" }         // Before/after compliance report
];

// === Dashboard Component ===
export default function Dashboard({ user, onLogout }) {
  // Track currently active tab (default = "Pipeline Status")
  const [tab, setTab] = useState("status");

  // === RBAC: Restrict tab access by role ===
  // - Admin and Service Provider: full access
  // - Client: only status, frameworks, and risk diagram
  const roleTabs = TABS.filter(tabObj => {
    if (["admin", "Service Provider"].includes(user.role)) return true;
    // Client role: restrict to key read-only panels
    if (user.role === "Client") return ["status", "framework", "risk"].includes(tabObj.key);
    return false;
  });

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      {/* Header Bar: User + Logout */}
      <div className="flex justify-between mb-6">
        <h1 className="text-3xl font-bold">
          Welcome, {user.username} ({user.role})
        </h1>
        <button
          onClick={onLogout}
          className="text-sm bg-red-400 text-white p-2 rounded"
        >
          Logout
        </button>
      </div>

      {/* === Tab Navigation === */}
      <div className="mb-6 flex space-x-4">
        {roleTabs.map(tabObj => (
          <button
            key={tabObj.key}
            onClick={() => setTab(tabObj.key)}
            className={tab === tabObj.key ? "font-bold underline" : ""}
          >
            {tabObj.label}
          </button>
        ))}
      </div>

      {/* === Main Content: Panels Rendered By Tab === */}
      {tab === "status" && <PipelineStatus />}  {/* Live real-time backend agent status */}
      {tab === "framework" && <FrameworkUpload user={user} />}
      {tab === "arch" && user.role !== "Client" && <ArchitectureInput />}
      {tab === "eng" && ["admin", "Service Provider"].includes(user.role) && <EngineeringPanel />}
      {tab === "iam" && ["admin", "Service Provider"].includes(user.role) && <IamAuditPanel />}
      {tab === "risk" && <RiskDiagram />}
      {tab === "reason" && ["admin", "Service Provider"].includes(user.role) && <AgentReasoning />}
      {tab === "delta" && ["admin", "Service Provider"].includes(user.role) && <DeltaAnalysisPanel />}
    </div>
  );
}

// =============================================================================
//  HOW TO ADD MORE TABS / PANELS:
//    1. Add new { key, label } to TABS array above.
//    2. Add {tab === "yourkey" && <YourComponent />} in the render section.
//    3. Restrict by role (in roleTabs) if needed.
//
//  The code above makes access logic and UI wiring explicit for onboarding,
//  support, and future audits. Extend with confidence.
// =============================================================================