// This component serves as the main dashboard for the application, providing a user interface
// that allows users to navigate between different functionalities based on their roles.
// It includes a header with the user's name and role, a logout button, and a tabbed navigation system
// that displays different components depending on the selected tab.
// The component uses React's state management to handle the current tab and conditionally renders components
// based on the user's role, ensuring that only authorized users can access certain features.
// The Dashboard component is designed to be flexible and extensible, allowing for easy addition of new features
// and functionalities in the future.

import React, { useState } from "react";
import FrameworkUpload from "../components/FrameworkUpload.jsx";
import ArchitectureInput from "../components/ArchitectureInput.jsx";
import EngineeringPanel from "../components/EngineeringPanel.jsx";
import RiskDiagram from "../components/RiskDiagram.jsx";
import PipelineStatus from "../components/PipelineStatus.jsx";
import AgentReasoning from "../components/AgentReasoning.jsx";

const TABS = [
  { key: "status", label: "Pipeline Status" },
  { key: "framework", label: "Frameworks" },
  { key: "arch", label: "Architecture" },
  { key: "eng", label: "Engineering" },
  { key: "risk", label: "Risk Diagram" },
  { key: "reason", label: "Agent Reasoning" }
];

export default function Dashboard({ user, onLogout }) {
  const [tab, setTab] = useState("status");

  // RBAC visibility
  const roleTabs = TABS.filter(tabObj => {
    if (user.role === "admin") return true;
    if (user.role === "operator") return tabObj.key !== "reason";
    if (user.role === "viewer") return ["status", "framework", "risk"].includes(tabObj.key);
    return false;
  });

  return (
    <div className="min-h-screen bg-gray-100 p-8">
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
      {tab === "status" && <PipelineStatus />}
      {tab === "framework" && <FrameworkUpload user={user} />}
      {tab === "arch" && user.role !== "viewer" && <ArchitectureInput />}
      {tab === "eng" && user.role === "admin" && <EngineeringPanel />}
      {tab === "risk" && <RiskDiagram />}
      {tab === "reason" && user.role === "admin" && <AgentReasoning />}
    </div>
  );
}
