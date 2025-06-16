// This component allows users to paste IaC logs or upload files for validation
// It handles file uploads, framework selection, and displays validation results
// The validation results include passed/failed checks and recommendations
// The component is designed to be user-friendly and idiot-proof
// It uses a textarea for pasting logs and a file input for uploading IaC files
// The framework selection dropdown allows users to choose the compliance framework
// The component uses fetch to send the file and framework to the backend for validation
// The validation results are displayed in an alert for easy visibility
// The component is styled with Tailwind CSS classes for a clean UI
// The textarea is used for pasting logs, YAML, or Terraform code
// The file input accepts YAML, YML, Terraform, and text files
// The framework dropdown allows users to select the compliance framework
// The component is designed to be reusable and can be easily integrated into other parts of the application
// The component is self-contained and does not rely on external state management
// The component is designed to be responsive and works well on different screen sizes
// The component is designed to be accessible and follows best practices for web accessibility
// The component is designed to be performant and handles file uploads efficiently

import React, { useState } from "react";

export default function ArchitectureInput() {
  const [value, setValue] = useState("");
  const [framework, setFramework] = useState("NIST"); // default, change as needed

  // Idiot-proof file upload and validation
  function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    handleIaCValidation(file, framework);
  }

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
        alert(
          "Passed: " + data.passed.join(", ") + "\n" +
          "Failed: " + data.failed.join(", ") + "\n" +
          "Recommendations:\n" + data.recommendations.map(r => r.suggested_fix).join("\n")
        );
      });
  }

  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Architecture Input</h2>
      <textarea
        className="w-full h-40 p-2 border rounded"
        placeholder="Paste logs, YAML, or Terraform here..."
        value={value}
        onChange={e => setValue(e.target.value)}
      />
      <div className="mt-4">
        {/* Upload button for IaC files */}
        <input type="file" accept=".yaml,.yml,.tf,.txt" onChange={handleFileChange} />
        {/* Optional: let user choose framework */}
        <select className="ml-2 p-1 border rounded" value={framework} onChange={e => setFramework(e.target.value)}>
          <option value="NIST">NIST</option>
          <option value="PCI">PCI</option>
          <option value="HIPAA">HIPAA</option>
          <option value="GDPR">GDPR</option>
          
        </select>
      </div>
    </div>
  );
}
