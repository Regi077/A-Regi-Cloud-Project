// =============================================================================
//  DeltaAnalysisPanel.jsx -- UI for Delta Analysis & PDF Export
// =============================================================================
//  Author: Reginald
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Provides a user-friendly interface for comparing JSON objects before and after remediation.
//    - Visualizes pass/fail status for each field and enables export of results as a PDF report.
//    - Supports error handling, clear state management, and integrates with backend microservice.
//
//  KEY FEATURES:
//    - Two textarea inputs for pre- and post-remediation JSON.
//    - 'Compare' button: calls backend to compute field-level delta analysis.
//    - Pass %, detailed changes, and recommendations rendered for easy review.
//    - 'Export as PDF' button: calls backend to generate and download a PDF summary.
//    - Tailwind CSS for modern, accessible styling.
//
//  INTEGRATION NOTES:
//    - Expects backend delta-analysis service running at http://localhost:5050.
//    - Easy to extend: can embed as a dashboard tab or as a standalone report UI.
// =============================================================================

import React, { useState } from "react";

export default function DeltaAnalysisPanel() {
  const [pre, setPre] = useState("");       // For pre-remediation JSON
  const [post, setPost] = useState("");     // For post-remediation JSON
  const [result, setResult] = useState(null); // For analysis results
  const [error, setError] = useState("");     // Error state

  // Compare button handler
  function handleCompare() {
    let preObj, postObj;
    try {
      preObj = JSON.parse(pre);
      postObj = JSON.parse(post);
    } catch {
      setError("Invalid JSON. Please check your input.");
      return;
    }
    setError(""); // Clear previous error
    // Call backend with pre and post JSON
    fetch("http://localhost:5050/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pre: preObj,
        post: postObj
      })
    })
      .then(res => res.json())
      .then(data => setResult(data));
  }

  // Export PDF button handler
  function handleExport() {
    fetch("http://localhost:5050/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ delta: result })
    })
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "delta_report.pdf";
        a.click();
      });
  }

  // =============================================================================
  //  Main UI: Input areas, compare/export controls, and delta results
  // =============================================================================

  return (
    <div className="p-6 bg-white rounded shadow">
      <h2 className="font-bold text-xl mb-4">Delta Analysis</h2>

      {/* Pre-remediation JSON input */}
      <div className="mb-2">
        <label>Pre-remediation JSON:</label>
        <textarea
          className="w-full h-24 p-2 border rounded mb-2"
          value={pre}
          onChange={e => setPre(e.target.value)}
          placeholder='Paste pre-remediation JSON here'
        />
      </div>

      {/* Post-remediation JSON input */}
      <div className="mb-2">
        <label>Post-remediation JSON:</label>
        <textarea
          className="w-full h-24 p-2 border rounded"
          value={post}
          onChange={e => setPost(e.target.value)}
          placeholder='Paste post-remediation JSON here'
        />
      </div>

      {/* Error message */}
      {error && (
        <div className="text-red-600 font-semibold mb-2">{error}</div>
      )}

      {/* Compare Button */}
      <button
        className="mt-2 bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleCompare}
      >
        Compare
      </button>

      {/* Results and Export */}
      {result && (
        <div className="mt-4">
          <b>Pass %:</b> {result.pass_pct}%<br/>
          <b>Fields Passed:</b> {result.passed.join(", ") || "None"}<br/>
          <b>Fields Failed:</b> {result.failed.join(", ") || "None"}
          <ul className="mt-2">
            {result.changes.map((chg, i) => (
              <li key={i}>
                {chg.field}: {String(chg.before)} → {String(chg.after)}
              </li>
            ))}
          </ul>
          <button
            className="mt-2 bg-green-600 text-white px-4 py-1 rounded"
            onClick={handleExport}
          >
            Export as PDF
          </button>
        </div>
      )}
    </div>
  );
}

// =============================================================================
//  End of DeltaAnalysisPanel.jsx -- Hassle-free, results-focused delta analysis UI
// =============================================================================
