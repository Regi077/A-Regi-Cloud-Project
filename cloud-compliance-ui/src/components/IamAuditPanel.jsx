// =============================================================================
//  IamAuditPanel.jsx -- Interactive IAM Audit UI Component
// =============================================================================
//  Author: Reginald 
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Provides a user interface for uploading or pasting IAM policy JSON for security auditing.
//    - Connects directly to Phase 6 backend microservice (port 5040) to perform audits.
//    - Displays color-coded risk scores and human-readable audit findings in real time.
//    - Designed for ease of use, smooth onboarding, and minimal error risk.
//
//  HOW IT WORKS:
//    - User uploads a .json file *or* pastes IAM JSON directly into a textarea.
//    - On "Audit IAM" button click, input is validated and POSTed to the backend endpoint.
//    - Displays high/medium/low risk counts and full details with clear visual cues.
//    - Handles file errors, JSON validation, and backend failures gracefully.
//
//  KEY FEATURES:
//    - UI with clear instructions and feedback.
//    - Rich color coding for risk (red/yellow/green).
//    - No external state or dependencies: easy to drop into any React dashboard.
//
//  INTEGRATION NOTES:
//    - Backend microservice must be running at http://localhost:5040/audit-iam.
//    - To extend: add more fields, tweak risk color logic, or support bulk audits.
// =============================================================================

import React, { useState } from "react";

// Utility for color-coding risk in audit results
function riskColor(risk) {
  if (risk === "High") return "text-red-600 font-bold";
  if (risk === "Medium") return "text-yellow-600 font-bold";
  return "text-green-600 font-bold";
}

export default function IamAuditPanel() {
  const [input, setInput] = useState("");      // IAM JSON text (manual paste or file upload)
  const [result, setResult] = useState(null);  // Audit results from backend
  const [error, setError] = useState("");      // Any user or backend error

  // Handles file uploads (reads file, puts content in textarea, clears errors)
  function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      setInput(e.target.result); // Show uploaded file in textarea for transparency
      setError("");
    };
    reader.onerror = () => setError("Failed to read file. Please try another file.");
    reader.readAsText(file);
  }

  // Handles clicking "Audit IAM": parses JSON, sends to backend, processes response
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
      .then(data => setResult(data))
      .catch(() => setError("Failed to audit IAM JSON!"));
  }

  // =============================================================================
  //  Main UI: File upload, textarea, Audit button, results, and error feedback
  // =============================================================================

  return (
    <div className="p-6 bg-white rounded shadow">
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
//  End of IamAuditPanel.jsx -- Secure, user-friendly IAM risk auditing panel
// =============================================================================
