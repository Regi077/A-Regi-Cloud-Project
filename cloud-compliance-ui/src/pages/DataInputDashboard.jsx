// =============================================================================
//  DataInputDashboard.jsx -- Unified Data Input Panel (Framework, Architecture, IAM)
// =============================================================================
//  Author: Reginald
//
//  DESCRIPTION:
//    - Merges FrameworkUpload, ArchitectureInput, and IamAuditPanel into one dashboard.
//    - PipelineStatus bar is always visible at the top for live agent feedback.
//    - User can tab between Framework Upload, Architecture Input, IAM Audit.
//
//  HOW TO EXTEND:
//    - To add more input methods, add another tab+panel below.
//    - Logic and styling are explicit for fast onboarding and dev confidence.
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
export default function DataInputDashboard() {
  // Track which input panel is active
  const [tab, setTab] = useState("framework");

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
        {tab === "framework" && <FrameworkUpload />}
        {tab === "architecture" && <ArchitectureInput />}
        {tab === "iam" && <IamAuditPanel />}
      </div>
    </div>
  );
}

// =============================================================================
//  End of DataInputDashboard.jsx -- All user input in one panel, live agent status always on
// =============================================================================
