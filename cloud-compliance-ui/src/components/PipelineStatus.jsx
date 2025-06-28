// =============================================================================
//  PipelineStatus.jsx -- Real-Time Pipeline Agent Status Panel (React)
// =============================================================================
//  Author: Reginald
//
//  DESCRIPTION:
//    - Displays live status for all pipeline agents (Ingestion, Validation, etc.)
//    - Integrates with backend dashboard via Socket.IO for instant updates.
//    - Uses color-coded status bubbles and strong, readable text for clarity.
//    - All mapping logic and display configs are at the top for easy extension.
//
//  HOW TO EXTEND / MAINTAIN:
//    - Add new pipeline names to `pipelineNames` and `topicToName` as you add more services.
//    - Adjust status normalization in `normalizeStatus()` if backend changes vocabulary.
//    - All style, mapping, and logic changes are isolated and clearly labeled.
//
//  USAGE:
//    - Place this in your main dashboard or agent status section.
//    - No props or context required; works out of the box with your backend event topics.
// =============================================================================

import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";

// -----------------------------------------------------------------------------
// STATUS & PIPELINE MAPPINGS (Edit these when backend topics or pipelines change)
// -----------------------------------------------------------------------------

// PipelineStatus.jsx
const statusClassMap = {
  Idle: "bg-gray-400 border-gray-300",
  Running: "bg-yellow-400 border-yellow-300 animate-pulse",
  Success: "bg-green-500 border-green-300",
  Error: "bg-red-500 border-red-300"
};

const pipelineNames = [
  "Ingestion",
  "Validation",
  "Remediation",
  "IAM Audit",
  "Reporting"
];

const topicToName = {
  "rule-ingestion": "Ingestion",
  "framework-validator": "Validation",
  "iac-analysis": "Remediation",
  "iam-audit": "IAM Audit",
  "delta-analysis": "Reporting"
};

function normalizeStatus(status) {
  if (!status) return "Idle";
  const s = status.toLowerCase();
  if (s === "done" || s === "success") return "Success";
  if (s === "error" || s === "failed" || s === "fail") return "Error";
  if (s === "running" || s === "in_progress") return "Running";
  return "Idle";
}

// -----------------------------------------------------------------------------
// MAIN COMPONENT: PipelineStatus
// -----------------------------------------------------------------------------

export default function PipelineStatus() {
  const [pipelineStates, setPipelineStates] = useState(
    pipelineNames.map(name => ({ name, status: "Idle" }))
  );

  useEffect(() => {
    const socket = io("http://localhost:5001");
    socket.on("pipeline_update", (event) => {
      const displayName = topicToName[event.pipeline] || event.pipeline;
      const displayStatus = normalizeStatus(event.status);

      setPipelineStates(current =>
        current.map(p =>
          p.name === displayName ? { ...p, status: displayStatus } : p
        )
      );
    });
    return () => {
      socket.off("pipeline_update");
      socket.disconnect();
    };
  }, []);

  // ---------------------------------------------------------------------------
  //  UI: Smallest, Clear White Bubbles with Status Border, Ample Section Spacing
  // ---------------------------------------------------------------------------
  return (
    <div className="pipeline-container">
      <div className="flex flex-col items-center w-full">
        <h2 className="font-bold text-2xl mb-8 text-center">Pipeline Agent Status</h2>
        <div className="pipeline-bubble-container flex flex-row justify-center items-end w-full mb-20 gap-16">
          {pipelineStates.map(p => (
            <div
              key={p.name}
              className="flex flex-col items-center flex-1 min-w-[70px] list-none !m-0 !p-0"
            >
              <span
                className={`w-6 h-6 rounded-full border-4 shadow-lg mb-2 z-10 ${statusClassMap[p.status]}`}
                style={{ display: "inline-block" }}
                title={p.status}
              />
              <span className="text-base font-semibold mt-1">{p.name}</span>
            </div>
          ))}
        </div>
        {/* === Spacer for extra space below bubbles and before next section === */}
         <div className="w-full mt-100" />
         
      </div>


    </div>
  );
}

// =============================================================================
//  How This Works (For Future Onboarding):
//  - Connects to backend dashboard using Socket.IO for live pipeline events.
//  - Listens for "pipeline_update" and updates UI instantly for each agent.
//  - All display/status mappings are centralized for painless updates.
// =============================================================================

// =============================================================================
//  End of PipelineStatus.jsx -- Real-Time Pipeline Agent Status Panel (React)
// =============================================================================
