// =============================================================================
//  FrameworkUpload.jsx -- UI Component for Uploading Compliance Framework Files
// =============================================================================
//  Author: Reginald
//
//  DESCRIPTION:
//    - Lets users upload compliance framework files (PDF or TXT) to the backend ingestion pipeline.
//    - Accepts `onComplete` and `value` props for persistent state and LLM reasoning sync.
//    - Notifies parent dashboard on upload complete, so data is always in sync across tabs.
// =============================================================================

import React, { useState, useEffect } from "react";

export default function FrameworkUpload({ onComplete = () => {}, value = null }) {
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState(value); // Show parent state if available

  // Sync up with parent when "value" changes (e.g., after tab switch)
  useEffect(() => {
    if (value && value !== result) setResult(value);
    // If tab was cleared elsewhere, update here too
    if (!value && result) setResult(null);
  }, [value]);

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
      .then(data => {
        setResult(data);
        onComplete(data); // Notify parent for sync
      })
      .catch(err => {
        setResult({ error: err.message });
        onComplete({ error: err.message }); // Also notify parent
      });
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
//  End of FrameworkUpload.jsx -- Hassle-free compliance framework uploader (persistent)
// =============================================================================
