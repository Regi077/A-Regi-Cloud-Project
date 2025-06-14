
// This component displays the status of various pipeline stages with color-coded indicators.
// It uses a simple array to represent the pipeline states and their statuses, which can be extended or modified as needed.     
// The colors are defined in an object for easy reference, allowing for quick updates if new statuses are added.


import React from "react";
const pipelineStates = [
  { name: "Ingestion", status: "Idle" },
  { name: "Validation", status: "Running" },
  { name: "Remediation", status: "Idle" },
  { name: "IAM Audit", status: "Idle" },
  { name: "Reporting", status: "Success" }
];
const colors = { "Idle": "gray", "Running": "yellow", "Success": "green", "Error": "red" };

export default function PipelineStatus() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Pipeline Agent Status</h2>
      <ul>
        {pipelineStates.map(p => (
          <li key={p.name} className="flex items-center mb-2">
            <span className={`w-3 h-3 mr-2 rounded-full bg-${colors[p.status]}-500`}></span>
            <span className="mr-4">{p.name}</span>
            <span className={`text-${colors[p.status]}-700 font-semibold`}>{p.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

