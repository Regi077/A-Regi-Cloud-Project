// =============================================================================
//  AgentReasoning.jsx -- Cloud Compliance Agent Reasoning Trace Component
// =============================================================================
//  Author: Reginald 
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Displays the step-by-step "thought process" or decision trace of the AI/agent.
//    - Each step mimics what a human or LLM agent might consider while reviewing
//      compliance framework requirements versus organizational policies.
//    - Hardcoded for demo purposes, but structured for easy extension to dynamic data.
//
//  USAGE:
//    - Import and include <AgentReasoning /> in your dashboard or any panel.
//    - In production, replace the static `reasoning` array with data pulled from
//      the backend (e.g., LLM-generated or pipeline logs).
//
// =============================================================================

import React from "react";

// Example reasoning steps for demo and onboarding
const reasoning = [
  { step: "Thought", desc: "Should check NIST password length policy" },
  { step: "Action", desc: "Parsed framework PDF for password policy section" },
  { step: "Observation", desc: "Found: Min length 12" },
  { step: "Thought", desc: "Compare to org's current policy (min 8)" },
  { step: "Action", desc: "Flagged as non-compliant, recommended remediation" },
  { step: "Final Verdict", desc: "Display recommendation in Engineering panel" }
];

// Main export: AgentReasoning component
export default function AgentReasoning() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Agent Reasoning Trace</h2>
      <ol className="list-decimal ml-6">
        {reasoning.map((r, idx) => (
          <li key={idx} className="mb-2">
            <b>{r.step}:</b> {r.desc}
          </li>
        ))}
      </ol>
    </div>
  );
}

// =============================================================================
//  End of AgentReasoning.jsx -- Clean, human-readable trace for dev & user insight
// =============================================================================
