import React, { useState } from "react";

// Utility for color-coding risk
function riskColor(risk) {
  if (risk === "High") return "text-red-600 font-bold";
  if (risk === "Medium") return "text-yellow-600 font-bold";
  return "text-green-600 font-bold";
}

export default function IamAuditPanel() {
  const [input, setInput] = useState("");     // For textarea paste
  const [result, setResult] = useState(null); // For backend results
  const [error, setError] = useState("");     // For error messages

  // Handle file upload (reads and sets textarea too)
  function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      setInput(e.target.result); // show file content in textarea
      setError("");
    };
    reader.onerror = () => setError("Failed to read file. Please try another file.");
    reader.readAsText(file);
  }

  // Handle audit action (from textarea)
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

  return (
    <div className="p-6 bg-white rounded shadow">
      <h2 className="font-bold text-xl mb-4">IAM Audit</h2>
      
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
      
      <div className="mb-3">
        <label className="block font-semibold mb-1">Or paste/edit IAM JSON:</label>
        <textarea
          className="w-full h-40 p-2 border rounded"
          placeholder='Paste your IAM JSON here'
          value={input}
          onChange={e => setInput(e.target.value)}
        />
      </div>
      
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleAudit}
        disabled={!input.trim()}
      >
        Audit IAM
      </button>

      {error && (
        <div className="mt-3 text-red-600 font-semibold">{error}</div>
      )}

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
// This component allows users to upload a JSON file or paste IAM JSON directly.
// It sends the JSON to a backend endpoint for auditing and displays the results.
// The results include risk levels and detailed issues, color-coded for easy identification.
// The component also handles errors gracefully, providing feedback to the user.
// The riskColor function is used to apply different text colors based on the risk level.
// The component is styled using Tailwind CSS for a clean and modern look.
// The component is designed to be user-friendly, with clear labels and instructions.
// The handleFile function reads the uploaded file and sets its content in the textarea.