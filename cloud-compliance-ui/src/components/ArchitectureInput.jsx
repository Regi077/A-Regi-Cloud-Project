// =============================================================================
//  ArchitectureInput.jsx -- Cloud Compliance: Architecture Upload & Validation UI
// =============================================================================
//  Author: Reginald
//
//  PURPOSE:
//    - Persistent state for data input; works seamlessly when switching tabs.
//    - Notifies parent dashboard of results for LLM agent sync and display.
// =============================================================================

import React, { useState, useEffect } from "react";

export default function ArchitectureInput({ onComplete = () => {}, value = null }) {
  // Restore last submission if switching back to this tab
  const [textValue, setTextValue] = useState("");
  const [framework, setFramework] = useState("NIST");
  const [lastResult, setLastResult] = useState(value);

  // --- Keep input/result in sync with parent state on tab switch ---
  useEffect(() => {
    if (value && value !== lastResult) {
      setLastResult(value);
      // Optionally, restore textarea if you want (up to your UX preference)
      // setTextValue(""); // Leave as-is for now.
    }
  }, [value]);

  // Handles file upload events (idiot-proof: only submits if file is selected)
  function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    handleIaCValidation(file, framework);
  }

  // Submit pasted logs or IaC as a string (if user uses textarea)
  function handlePasteValidation() {
    if (!textValue.trim()) return alert("Paste or upload some IaC/log data first.");
    const formData = new FormData();
    // For backend, you may want a special key for raw text
    formData.append("iac", new Blob([textValue], { type: "text/plain" }));
    formData.append("framework", framework);

    fetch("http://localhost:5020/validate-framework", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        setLastResult(data);
        onComplete(data); // Notify parent for LLM agent sync
        alert(
          "Passed: " + (data.passed || []).join(", ") + "\n" +
          "Failed: " + (data.failed || []).join(", ") + "\n" +
          "Recommendations:\n" +
          ((data.recommendations || []).map(r => r.suggested_fix).join("\n") || "None")
        );
      });
  }

  // Calls backend API to validate the uploaded IaC file against selected framework
  function handleIaCValidation(file, framework) {
    const formData = new FormData();
    formData.append("iac", file);
    formData.append("framework", framework);

    fetch("http://localhost:5020/validate-framework", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        setLastResult(data);
        onComplete(data);
        alert(
          "Passed: " + (data.passed || []).join(", ") + "\n" +
          "Failed: " + (data.failed || []).join(", ") + "\n" +
          "Recommendations:\n" +
          ((data.recommendations || []).map(r => r.suggested_fix).join("\n") || "None")
        );
      });
  }

  // =============================================================================
  //  UI Layout -- Simple, responsive, persistent
  // =============================================================================
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Architecture Input</h2>
      {/* Textarea for logs, YAML, or Terraform */}
      <textarea
        className="w-full h-40 p-2 border rounded"
        placeholder="Paste logs, YAML, or Terraform here..."
        value={textValue}
        onChange={e => setTextValue(e.target.value)}
      />
      <div className="mt-4">
        {/* Idiot-proof file upload control */}
        <input type="file" accept=".yaml,.yml,.tf,.txt" onChange={handleFileChange} />
        {/* Framework selection dropdown (extend as needed) */}
        <select
          className="ml-2 p-1 border rounded"
          value={framework}
          onChange={e => setFramework(e.target.value)}
        >
          <option value="NIST">NIST</option>
          <option value="PCI">PCI</option>
          <option value="HIPAA">HIPAA</option>
          <option value="GDPR">GDPR</option>
        </select>
        {/* Button to submit pasted text */}
        <button
          onClick={handlePasteValidation}
          className="ml-2 bg-blue-500 text-white px-4 py-2 rounded"
        >
          Validate Pasted Text
        </button>
      </div>
      {/* Show last result if present and tab is revisited */}
      {lastResult && (
        <div className="mt-4 p-2 bg-gray-100 rounded">
          <pre>{JSON.stringify(lastResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

// =============================================================================
//  End of ArchitectureInput.jsx -- Hassle-free, user-friendly validation UI (persistent)
// =============================================================================
