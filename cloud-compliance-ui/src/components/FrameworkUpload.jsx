
// This component allows users to upload compliance framework files.


import React, { useState } from "react";
export default function FrameworkUpload() {
  const [files, setFiles] = useState([]);
  function handleChange(e) {
    setFiles([...files, ...Array.from(e.target.files)]);
  }
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Upload Compliance Framework</h2>
      <input type="file" multiple accept=".pdf,.txt" onChange={handleChange} />
      <ul className="mt-4">{files.map(f => <li key={f.name}>{f.name}</li>)}</ul>
    </div>
  );
}

  