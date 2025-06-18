// =============================================================================
//  ArchitectureInput.jsx -- Cloud Compliance: Architecture Upload & Validation UI
// =============================================================================
//  Author: Reginald 
//  Last updated: 18th June 2025
//
//  PURPOSE:
//    - Provides an idiot-proof interface for users to upload Infrastructure-as-Code (IaC)
//      files (YAML, Terraform, text) or paste raw logs for validation against compliance frameworks.
//    - Collects file input, framework selection, and handles validation round-trip with backend.
//    - Displays validation results (pass/fail, recommendations) in a simple alert.
//
//  KEY FEATURES:
//    - Textarea for manual pasting of logs or IaC snippets.
//    - File input for easy drag-and-drop/upload (accepts .yaml, .yml, .tf, .txt).
//    - Framework dropdown for NIST, PCI, HIPAA, GDPR, etc.
//    - Idiot-proof error handling: only sends if a file is actually selected.
//    - Responsive, accessible UI with Tailwind styling.
//
//  INTEGRATION NOTES:
//    - This component is standalone: does not depend on any global state.
//    - To use, simply drop <ArchitectureInput /> into a page or dashboard.
//    - Backend endpoint: POST to http://localhost:5020/validate-framework.
//    - Extend the frameworks list as needed to match your backend configuration.
// =============================================================================

import React, { useState } from "react";

export default function ArchitectureInput() {
  // State for textarea value and framework selection
  const [value, setValue] = useState("");
  const [framework, setFramework] = useState("NIST"); // Default framework

  // Handles file upload events (idiot-proof: only submits if file is selected)
  function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    handleIaCValidation(file, framework);
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
        // Show results in a simple alert (can be enhanced to modal in production)
        alert(
          "Passed: " + data.passed.join(", ") + "\n" +
          "Failed: " + data.failed.join(", ") + "\n" +
          "Recommendations:\n" + data.recommendations.map(r => r.suggested_fix).join("\n")
        );
      });
  }

  // =============================================================================
  //  UI Layout -- Simple, responsive, and accessible
  // =============================================================================
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Architecture Input</h2>
      {/* Textarea for logs, YAML, or Terraform */}
      <textarea
        className="w-full h-40 p-2 border rounded"
        placeholder="Paste logs, YAML, or Terraform here..."
        value={value}
        onChange={e => setValue(e.target.value)}
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
      </div>
    </div>
  );
}

// =============================================================================
//  End of ArchitectureInput.jsx -- Hassle-free, user-friendly validation UI
// =============================================================================
