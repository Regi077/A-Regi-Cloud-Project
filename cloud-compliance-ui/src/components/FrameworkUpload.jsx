// =============================================================================
//  FrameworkUpload.jsx -- UI Component for Uploading Compliance Framework Files
// =============================================================================
//  Author: Reginald 
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Lets users upload compliance framework files (PDF or TXT) to the backend ingestion pipeline.
//    - Integrates directly with Phase 3 microservice at :5010/ingest-doc.
//    - Handles file selection, error feedback, upload confirmation, and response display.
//    - Designed for clarity, ease of use, and seamless onboarding for new developers.
//
//  HOW IT WORKS:
//    - User selects a file (only first file used if multiple selected).
//    - Clicks Upload to POST the file to backend.
//    - Displays upload result (success or error) with clear feedback.
//    - Ready to embed as a dashboard tab or as a standalone component.
//
//  NOTES:
//    - Backend endpoint (http://localhost:5010/ingest-doc) must be running.
//    - All state management is local; does not require external props/context.
// =============================================================================

import React, { useState } from "react";

export default function FrameworkUpload() {
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState(null);

  // Update state when files are selected
  function handleChange(e) {
    setFiles([...e.target.files]);
    setResult(null); // Reset result when a new file is chosen
  }

  // Handles upload to backend (only the first file is used)
  function handleUpload() {
    if (files.length === 0) return alert("Please select a file.");

    const file = files[0];
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:5010/ingest-doc", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => setResult(data))
      .catch(err => setResult({ error: err.message }));
  }

  // =============================================================================
  //  Main UI -- File input, upload button, filename preview, upload results
  // =============================================================================

  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Upload Compliance Framework</h2>
      {/* File input (PDF/TXT only) */}
      <input
        type="file"
        accept=".pdf,.txt"
        onChange={handleChange}
      />
      {/* Upload button */}
      <button
        onClick={handleUpload}
        className="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
      {/* List selected files */}
      <ul className="mt-4">
        {files.map(f => <li key={f.name}>{f.name}</li>)}
      </ul>
      {/* Display upload result or error */}
      {result && (
        <div className="mt-4 p-2 bg-gray-100 rounded">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

// =============================================================================
//  End of FrameworkUpload.jsx -- Hassle-free compliance framework uploader
// =============================================================================
