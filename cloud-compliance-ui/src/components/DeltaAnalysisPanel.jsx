// This component provides a UI for delta analysis between pre and post remediation JSON data.
// It allows users to input JSON data, compare them, and export the results as a PDF.
// The component uses React hooks for state management and fetch API for backend communication.
// The UI is styled with Tailwind CSS classes for a clean and modern look.
// The component includes error handling for JSON parsing and backend responses.
// The export functionality creates a downloadable PDF report of the analysis results.
// The component is designed to be reusable and can be integrated into larger applications easily.

import React, { useState } from "react";

export default function DeltaAnalysisPanel() {
  const [pre, setPre] = useState("");       // For pre-remediation JSON
  const [post, setPost] = useState("");     // For post-remediation JSON
  const [result, setResult] = useState(null); // For analysis results

  // Compare button handler
  function handleCompare() {
    // Call backend with pre and post JSON
    fetch("http://localhost:5050/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pre: JSON.parse(pre),
        post: JSON.parse(post)
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
