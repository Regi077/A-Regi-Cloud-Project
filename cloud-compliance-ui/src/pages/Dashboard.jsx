// =============================================================================
//  Dashboard.jsx -- Executive, Hassle-Free Compliance UI Main Panel
// =============================================================================
//  Author: Reginald 
//
//  DESCRIPTION:
//    - Central dashboard with tabbed navigation for all compliance workflows.
//    - Role-based access control: panels/tabs rendered based on user.role.
//    - DataInputDashboard: Merges FrameworkUpload, ArchitectureInput, IamAuditPanel, with PipelineStatus always visible.
//    - Shares state for input and reasoning trace so tabs never lose data.
// =============================================================================

import React, { useState } from "react";
import DataInputDashboard from "./DataInputDashboard.jsx";
import AgentReasoning from "../components/AgentReasoning.jsx";
import EngineeringPanel from "../components/EngineeringPanel.jsx";
import DeltaAnalysisPanel from "../components/DeltaAnalysisPanel.jsx";
import RiskDiagram from "../components/RiskDiagram.jsx";

// === Tab Definitions: New order as requested ===
const TABS = [
  { key: "datainput", label: "Data Input" },         // NEW merged input panel
  { key: "reason", label: "Agent Reasoning" },       // Agent's thought process & decision tree
  { key: "eng", label: "Engineering" },              // Remediation suggestions, accept/reject
  { key: "delta", label: "Delta Analysis" },         // Before/after compliance report
  { key: "risk", label: "Risk Diagram" }             // Visualization of risk/priorities
];

// === Dashboard Component ===
export default function Dashboard({ user, onLogout }) {
  // Default tab = "Data Input" for best onboarding
  const [tab, setTab] = useState("datainput");

  // === Shared state: Agent reasoning trace and user input (persists across tabs) ===
  const [reasoningSteps, setReasoningSteps] = useState([]);  // [{step, desc, at}]
  const [inputData, setInputData] = useState({});            // {framework, architecture, iam}

  // RBAC: Full access for Admin/Service Provider, restricted for Client
  const roleTabs = TABS.filter(tabObj => {
    if (["admin", "Service Provider"].includes(user.role)) return true;
    // Client role: restrict to key read-only panels
    if (user.role === "Client") return ["datainput", "risk"].includes(tabObj.key);
    return false;
  });

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-8">
      {/* Header Bar: User + Logout */}
      <div className="flex justify-between items-center w-full max-w-5xl mb-6">
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
      <div className="mb-6 flex space-x-4 w-full max-w-5xl justify-center">
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

      {/* === Main Content: Panels Rendered By Tab, centered === */}
      <div className="flex-grow w-full max-w-5xl flex flex-col items-center">
        {tab === "datainput" && (
          <DataInputDashboard
            inputData={inputData}
            setInputData={setInputData}
            setReasoningSteps={setReasoningSteps}
          />
        )}
        {tab === "reason" && (
          <AgentReasoning
            reasoningSteps={reasoningSteps}
            inputData={inputData}
          />
        )}
        {tab === "eng" && ["admin", "Service Provider"].includes(user.role) && <EngineeringPanel />}
        {tab === "delta" && ["admin", "Service Provider"].includes(user.role) && <DeltaAnalysisPanel />}
        {tab === "risk" && <RiskDiagram />}
      </div>
    </div>
  );
}

// =============================================================================
//  HOW TO ADD MORE TABS / PANELS:
//    1. Add new { key, label } to TABS array above.
//    2. Add {tab === "yourkey" && <YourComponent />} in the render section.
//    3. Restrict by role (in roleTabs) if needed.
// =============================================================================
