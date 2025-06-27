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

// Static mapping: status to full Tailwind class (avoids dynamic class pitfalls)
const statusClassMap = {
  Idle:    "bg-gray-400 border-gray-300",
  Running: "bg-yellow-400 border-yellow-300 animate-pulse",
  Success: "bg-green-500 border-green-300",
  Error:   "bg-red-500 border-red-300"
};

// List of pipeline stages in UI order
const pipelineNames = [
  "Ingestion",
  "Validation",
  "Remediation",
  "IAM Audit",
  "Reporting"
];

// Map backend topic (from event.payload.pipeline) to display name in UI
const topicToName = {
  "rule-ingestion": "Ingestion",
  "framework-validator": "Validation",
  "iac-analysis": "Remediation",
  "iam-audit": "IAM Audit",
  "delta-analysis": "Reporting"
};

// Normalizes backend status to one of the four display statuses
function normalizeStatus(status) {
  if (!status) return "Idle";
  const s = status.toLowerCase();
  if (s === "done" || s === "success") return "Success";
  if (s === "error" || s === "failed" || s === "fail") return "Error";
  if (s === "running" || s === "in_progress") return "Running";
  return "Idle"; // Fallback/default
}

// -----------------------------------------------------------------------------
// MAIN COMPONENT: PipelineStatus
// -----------------------------------------------------------------------------

export default function PipelineStatus() {
  // Pipeline state array, one entry per pipeline agent (name + status)
  const [pipelineStates, setPipelineStates] = useState(
    pipelineNames.map(name => ({ name, status: "Idle" }))
  );

  useEffect(() => {
    // Connect to backend Socket.IO server for live updates
    const socket = io("http://localhost:5001");

    // Handle "pipeline_update" event (emitted by backend on any pipeline progress)
    socket.on("pipeline_update", (event) => {
      /*
        Expected event format:
        {
          pipeline: "rule-ingestion", // backend pipeline name (matches topicToName)
          status: "done" | "running" | "error" | ...
        }
      */
      const displayName = topicToName[event.pipeline] || event.pipeline;
      const displayStatus = normalizeStatus(event.status);

      setPipelineStates(current =>
        current.map(p =>
          p.name === displayName ? { ...p, status: displayStatus } : p
        )
      );
    });

    // Cleanup: remove listener and disconnect socket on unmount
    return () => {
      socket.off("pipeline_update");
      socket.disconnect();
    };
  }, []);

  // ---------------------------------------------------------------------------
  //  UI: Large, Clean Bubbles Row with Labels Below, Legend at Bottom
  //  [AI-ADD] Updated per latest step-by-step reference for executive visuals.
  // ---------------------------------------------------------------------------
  return (
    <div className="flex flex-col items-center w-full">
      <div className="bg-white rounded-2xl shadow-lg p-6 w-full max-w-xl mx-auto mb-8">
        <h2 className="font-bold text-xl mb-8 text-center">Pipeline Agent Status</h2>
        {/* [AI-ADD] Bubbles row with labels below each bubble, evenly spaced */}
        <div className="flex flex-row justify-between w-full mb-16 px-8">
          {pipelineStates.map(p => (
            <div key={p.name} className="flex flex-col items-center flex-1">
              {/* [AI-ADD] Large, real colored bubble (not a bullet) */}
              <span
                className={`w-8 h-8 rounded-full border-4 shadow-lg mb-2
                  ${statusClassMap[p.status] || "bg-gray-400 border-gray-300"}`}
                title={p.status}
              />
              <span className="text-lg font-medium">{p.name}</span>
            </div>
          ))}
        </div>
        {/* [AI-ADD] Status legend at bottom, clean, clear */}
        <div className="mt-6 flex gap-6 justify-center text-xs items-center">
          <span className="inline-block w-4 h-4 rounded-full bg-gray-400 border border-gray-300 mr-1" /> Idle
          <span className="inline-block w-4 h-4 rounded-full bg-yellow-400 animate-pulse border border-yellow-300 mr-1" /> Running
          <span className="inline-block w-4 h-4 rounded-full bg-green-500 border border-green-300 mr-1" /> Success
          <span className="inline-block w-4 h-4 rounded-full bg-red-500 border border-red-300 mr-1" /> Error
        </div>
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
