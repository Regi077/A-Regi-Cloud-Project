
// This component displays the reasoning trace of the agent's decision-making process.
// It includes steps like checking policies, parsing documents, and making recommendations.
// The reasoning is hardcoded for demonstration purposes, but in a real application,
// this could be dynamically generated based on the agent's actions and observations.


import React from "react";
const reasoning = [
  { step: "Thought", desc: "Should check NIST password length policy" },
  { step: "Action", desc: "Parsed framework PDF for password policy section" },
  { step: "Observation", desc: "Found: Min length 12" },
  { step: "Thought", desc: "Compare to org's current policy (min 8)" },
  { step: "Action", desc: "Flagged as non-compliant, recommended remediation" },
  { step: "Final Verdict", desc: "Display recommendation in Engineering panel" }
];

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


