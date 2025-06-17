// The Dashboard component provides a role-based user interface for navigating key features of the application.
// It displays a header with the user's name and role, a logout button, and a tab navigation bar.
// Tabs and their corresponding panels are shown or hidden based on the user's role, enforcing RBAC (Role-Based Access Control).
// The component uses React state to track the active tab and conditionally renders each panel accordingly.
// This structure ensures only authorized users can access sensitive features, while allowing for straightforward extension with new tabs or panels.
// The code emphasizes maintainability, clarity, and security through role-based conditional rendering.


import React, { useState } from "react";
import FrameworkUpload from "../components/FrameworkUpload.jsx";
import ArchitectureInput from "../components/ArchitectureInput.jsx";
import EngineeringPanel from "../components/EngineeringPanel.jsx";
import RiskDiagram from "../components/RiskDiagram.jsx";
import PipelineStatus from "../components/PipelineStatus.jsx";
import AgentReasoning from "../components/AgentReasoning.jsx";
import IamAuditPanel from "../components/IamAuditPanel.jsx"; // Import IAM Audit panel

const TABS = [
  { key: "status", label: "Pipeline Status" },
  { key: "framework", label: "Frameworks" },
  { key: "arch", label: "Architecture" },
  { key: "eng", label: "Engineering" },
  { key: "iam", label: "IAM Audit" },
  { key: "risk", label: "Risk Diagram" },
  { key: "reason", label: "Agent Reasoning" }
];

export default function Dashboard({ user, onLogout }) {
  const [tab, setTab] = useState("status");

  // RBAC: Full access for admin and Service Provider
  const roleTabs = TABS.filter(tabObj => {
    if (["admin", "Service Provider"].includes(user.role)) return true;
    if (user.role === "Client") return ["status", "framework", "risk"].includes(tabObj.key);
    return false;
  });

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      {/* Header */}
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
      {/* Tab navigation */}
      <div className="mb-6 flex space-x-4">
        {roleTabs.map(tabObj => (
          <button
            key={tabObj.key}
            onClick={() => setTab(tabObj.key)}
            className={tab === tabObj.key ? "font-bold" : ""}
          >
            {tabObj.label}
          </button>
        ))}
      </div>
      {/* Main dashboard content, by tab */}
      {tab === "status" && <PipelineStatus />}
      {tab === "framework" && <FrameworkUpload user={user} />}
      {tab === "arch" && user.role !== "Client" && <ArchitectureInput />}
      {tab === "eng" && ["admin", "Service Provider"].includes(user.role) && <EngineeringPanel />}
      {tab === "iam" && ["admin", "Service Provider"].includes(user.role) && <IamAuditPanel />}
      {tab === "risk" && <RiskDiagram />}
      {tab === "reason" && ["admin", "Service Provider"].includes(user.role) && <AgentReasoning />}
    </div>
  );
}
