// This component allows users to upload compliance framework files.
// Now uploads the actual file to /ingest-doc on port 5010 (Phase 3 backend).
// Allows upload of compliance frameworks to Phase 3 backend at :5010/ingest-doc.
// User must select a file and click Upload. Handles errors and shows result.

import React, { useState } from "react";

export default function FrameworkUpload() {
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState(null);

  // Update state with selected files
  function handleChange(e) {
    setFiles([...e.target.files]);
    setResult(null); // Clear previous result on new selection
  }

  // Upload first selected file to backend
  function handleUpload() {
    if (files.length === 0) return alert("Please select a file.");

    const file = files[0]; // Only first file for now
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

  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Upload Compliance Framework</h2>
      <input
        type="file"
        accept=".pdf,.txt"
        onChange={handleChange}
      />
      <button
        onClick={handleUpload}
        className="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
      <ul className="mt-4">
        {files.map(f => <li key={f.name}>{f.name}</li>)}
      </ul>
      {result && (
        <div className="mt-4 p-2 bg-gray-100 rounded">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
// Note: This component assumes the backend is running and accessible at the specified URL.
// Adjust the URL as needed for your environment.   
// The component handles file selection, upload, and displays the result or error message.
// It does not require any user prop or additional configuration.
// The file input accepts PDF and TXT files only, as specified in the requirements.
// The upload button triggers the upload process, and the result is displayed in a formatted JSON view.
// The component is designed to be clean and user-friendly, with clear instructions and feedback.
// The code is self-contained and does not rely on any external user data or props.
// It is ready to be integrated into a larger application or used as a standalone component.
// The component uses React hooks for state management and handles file uploads efficiently.