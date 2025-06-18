// =============================================================================
//  PipelineStatus.jsx -- Real-Time Pipeline Agent Status Panel (React)
// =============================================================================
//  Author: Reginald 
//  Last updated: 18th June 2025
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

// Status text to Tailwind color class mapping (only edit this for color changes)
const statusColors = {
  Idle: "gray",
  Running: "yellow",
  Success: "green",
  Error: "red"
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
// REUSABLE COMPONENT: StatusBubble (displays colored dot based on status)
// -----------------------------------------------------------------------------

function StatusBubble({ status }) {
  return (
    <span
      className={`w-3 h-3 mr-2 rounded-full bg-${statusColors[status] || "gray"}-500`}
      title={status}
    />
  );
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
  //  UI: Shows pipeline names, color-coded bubbles, and live status text
  // ---------------------------------------------------------------------------
  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h2 className="font-bold text-xl mb-4">Pipeline Agent Status</h2>
      <ul>
        {pipelineStates.map(p => (
          <li key={p.name} className="flex items-center mb-2">
            <StatusBubble status={p.status} />
            <span className="mr-4">{p.name}</span>
            <span className={`text-${statusColors[p.status] || "gray"}-700 font-semibold`}>
              {p.status}
            </span>
          </li>
        ))}
      </ul>
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