// =============================================================================
//  DataInputDashboard.jsx -- Unified Data Input Panel (Framework, Architecture, IAM)
// =============================================================================
//  Author: Reginald
//
//  DESCRIPTION:
//    - Merges FrameworkUpload, ArchitectureInput, and IamAuditPanel into one dashboard.
//    - PipelineStatus bar is always visible at the top for live agent feedback.
//    - User can tab between Framework Upload, Architecture Input, IAM Audit.
//    - Accepts props for persistent state handling (inputData, setInputData, setReasoningSteps).
// =============================================================================

import React, { useState } from "react";
import FrameworkUpload from "../components/FrameworkUpload.jsx";
import ArchitectureInput from "../components/ArchitectureInput.jsx";
import IamAuditPanel from "../components/IamAuditPanel.jsx";
import PipelineStatus from "../components/PipelineStatus.jsx";

// --- Tab Config: Each input type as a tab ---
const INPUT_TABS = [
  { key: "framework", label: "Compliance Framework Upload" },
  { key: "architecture", label: "Architecture/IaC Validation" },
  { key: "iam", label: "IAM Audit" }
];

// --- MAIN COMPONENT ---
export default function DataInputDashboard({
  inputData = {},
  setInputData = () => {},
  setReasoningSteps = () => {}
}) {
  // Track which input panel is active
  const [tab, setTab] = useState("framework");

  // --- Handlers to update state and trace reasoning ---
  function handleFrameworkUpload(result) {
    setInputData(data => ({ ...data, framework: result }));
    setReasoningSteps(steps => [
      ...steps,
      {
        step: "Framework Uploaded",
        result,
        at: new Date().toISOString()
      }
    ]);
  }
  function handleArchitectureInput(result) {
    setInputData(data => ({ ...data, architecture: result }));
    setReasoningSteps(steps => [
      ...steps,
      {
        step: "Architecture Uploaded",
        result,
        at: new Date().toISOString()
      }
    ]);
  }
  function handleIamAudit(result) {
    setInputData(data => ({ ...data, iam: result }));
    setReasoningSteps(steps => [
      ...steps,
      {
        step: "IAM Audit",
        result,
        at: new Date().toISOString()
      }
    ]);
  }

  return (
    <div className="w-full flex flex-col items-center">
      {/* === Always-on Pipeline Status (shows backend agent status at a glance) === */}
      <div className="w-full max-w-3xl">
        <PipelineStatus />
      </div>

      {/* === Input Tab Navigation (centered) === */}
      <div className="mt-8 mb-8 flex space-x-4 justify-center w-full max-w-3xl">
        {INPUT_TABS.map(tabObj => (
          <button
            key={tabObj.key}
            onClick={() => setTab(tabObj.key)}
            className={
              tab === tabObj.key
                ? "font-bold underline"
                : "text-gray-700"
            }
          >
            {tabObj.label}
          </button>
        ))}
      </div>

      {/* === Input Panels: Centered and on white card === */}
      <div className="w-full max-w-3xl flex flex-col items-center bg-white rounded shadow p-8">
        {tab === "framework" && (
          <FrameworkUpload
            onComplete={handleFrameworkUpload}
            value={inputData.framework}
          />
        )}
        {tab === "architecture" && (
          <ArchitectureInput
            onComplete={handleArchitectureInput}
            value={inputData.architecture}
          />
        )}
        {tab === "iam" && (
          <IamAuditPanel
            onComplete={handleIamAudit}
            value={inputData.iam}
          />
        )}
      </div>
    </div>
  );
}

// =============================================================================
//  End of DataInputDashboard.jsx -- All user input in one panel, live agent status always on
// =============================================================================
