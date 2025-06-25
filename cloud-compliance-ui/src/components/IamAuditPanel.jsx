// =============================================================================
//  IamAuditPanel.jsx -- Interactive IAM Audit UI Component (Persistent)
// =============================================================================
//  Author: Reginald
//
//  DESCRIPTION:
//    - Persistent IAM audit panel for use in unified Data Input dashboard.
//    - Notifies parent of audit results and restores last state when tab switches.
// =============================================================================

import React, { useState, useEffect } from "react";

// Utility for color-coding risk in audit results
function riskColor(risk) {
  if (risk === "High") return "text-red-600 font-bold";
  if (risk === "Medium") return "text-yellow-600 font-bold";
  return "text-green-600 font-bold";
}

export default function IamAuditPanel({ onComplete = () => {}, value = null }) {
  // State for IAM input and audit result
  const [input, setInput] = useState(value?.input || "");
  const [result, setResult] = useState(value?.result || null);
  const [error, setError] = useState("");

  // Restore last audit if parent passes a new value (tab switch)
  useEffect(() => {
    if (value && value.input !== undefined && value.input !== input) setInput(value.input);
    if (value && value.result !== undefined && value.result !== result) setResult(value.result);
    // eslint-disable-next-line
  }, [value]);

  // Handles file uploads
  function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      setInput(e.target.result);
      setError("");
    };
    reader.onerror = () => setError("Failed to read file. Please try another file.");
    reader.readAsText(file);
  }

  // Handles clicking "Audit IAM"
  function handleAudit() {
    setError("");
    let json;
    try {
      json = JSON.parse(input);
    } catch {
      setError("Invalid JSON! Please check your input.");
      return;
    }
    fetch("http://localhost:5040/audit-iam", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(json)
    })
      .then(res => {
        if (!res.ok) throw new Error("Server error");
        return res.json();
      })
      .then(data => {
        setResult(data);
        onComplete({ input, result: data }); // Sync up for Agent Reasoning trace
      })
      .catch(() => setError("Failed to audit IAM JSON!"));
  }

  // =============================================================================
  //  Main UI: File upload, textarea, Audit button, results, and error feedback
  // =============================================================================

  return (
    <div className="p-6 bg-white rounded shadow w-full">
      <h2 className="font-bold text-xl mb-4">IAM Audit</h2>
      
      {/* File Upload Section */}
      <div className="mb-3">
        <label className="block font-semibold mb-1">Upload .json file:</label>
        <input
          type="file"
          accept=".json,application/json"
          onChange={e => {
            if (e.target.files[0]) handleFile(e.target.files[0]);
          }}
          className="mb-2"
        />
      </div>
      
      {/* Manual Paste/Edit Section */}
      <div className="mb-3">
        <label className="block font-semibold mb-1">Or paste/edit IAM JSON:</label>
        <textarea
          className="w-full h-40 p-2 border rounded"
          placeholder='Paste your IAM JSON here'
          value={input}
          onChange={e => setInput(e.target.value)}
        />
      </div>
      
      {/* Trigger Audit Button */}
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleAudit}
        disabled={!input.trim()}
      >
        Audit IAM
      </button>

      {/* Error Display */}
      {error && (
        <div className="mt-3 text-red-600 font-semibold">{error}</div>
      )}

      {/* Results: risk counts and detailed findings */}
      {result && (
        <div className="mt-6">
          <p><b>High Risk:</b> {result.high_risk}</p>
          <p><b>Medium Risk:</b> {result.medium_risk}</p>
          <p><b>Low Risk:</b> {result.low_risk}</p>
          <ul className="mt-3">
            {result.details.map((r, i) => (
              <li key={i} className={`mb-1 ${riskColor(r.risk)}`}>
                <span>{r.risk}:</span> {r.issue}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// =============================================================================
//  End of IamAuditPanel.jsx -- Secure, user-friendly IAM risk auditing panel (persistent)
// =============================================================================
