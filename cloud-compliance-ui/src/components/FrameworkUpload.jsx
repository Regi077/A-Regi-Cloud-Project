
// This component allows users to upload compliance framework files.
// Note: This component assumes the backend is running on localhost:5000
// and that it has an endpoint /upload-doc that accepts POST requests with a JSON body containing the filename.   
// The user object is expected to have username and password properties for basic auth.
// The component uses basic file input handling and displays the result of the upload operation.  
// It also includes basic error handling to display any errors that occur during the upload process.


import React, { useState } from "react";

export default function FrameworkUpload({ user }) {
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState(null);

  function handleChange(e) {
    setFiles([...files, ...Array.from(e.target.files)]);
  }

  function handleUpload() {
    if (files.length === 0) return alert("Please select a file.");

    const file = files[0]; // Demo: only first file name for now

    fetch("http://localhost:5000/upload-doc", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Basic " + btoa(user.username + ":" + user.password)
      },
      body: JSON.stringify({ filename: file.name })
    })
      .then(res => res.json())
      .then(data => setResult(data))
      .catch(err => setResult({ error: err.message }));
  }

  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Upload Compliance Framework</h2>
      <input type="file" multiple accept=".pdf,.txt" onChange={handleChange} />
      <button
        onClick={handleUpload}
        className="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
      <ul className="mt-4">{files.map(f => <li key={f.name}>{f.name}</li>)}</ul>
      {result && (
        <div className="mt-4 p-2 bg-gray-100 rounded">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

