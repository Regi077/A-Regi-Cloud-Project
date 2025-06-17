// EngineeringPanel.jsx
// This component fetches remediation suggestions from the backend,
// allows user to Accept/Reject, and enables download of remediated IaC.
// Adapted for Azure. Idiot-proof and fully commented.

import React, { useEffect, useState } from "react";

export default function EngineeringPanel() {
  const [suggestions, setSuggestions] = useState([]);
  const [iacContent, setIacContent] = useState(""); 
  // Original IaC content (simulate here or fetch from backend/UI)
  const [remediatedIac, setRemediatedIac] = useState("");
  const [loading, setLoading] = useState(false);

  // Dummy: replace with your real IaC content or fetch from context/state
  useEffect(() => {
    setIacContent(
      'resource "azurerm_storage_account" "example" {\n  name = "mystorageaccount"\n  location = "eastus"\n}'
    );
  }, []);

  // Fetch suggestions from backend
  useEffect(() => {
    setLoading(true);
    // Dummy POST to backend; update endpoint and form data as needed
    fetch("http://localhost:5030/analyze-iac", {
      method: "POST",
      body: (() => {
        const fd = new FormData();
        // In real app, use file input or context/state for IaC file
        const blob = new Blob([iacContent], { type: "text/plain" });
        fd.append("iac", blob, "iac.tf");
        fd.append("framework", "Azure"); // Or allow user to select
        return fd;
      })(),
    })
      .then((res) => res.json())
      .then((data) => {
        setSuggestions(data.suggestions || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [iacContent]);

  // Accept a suggestion (append its block to the IaC and store)
  const handleAccept = (block) => {
    const updated = iacContent + "\n\n" + block;
    setRemediatedIac(updated);
    alert("Remediation block appended! Download below.");
  };

  // Download remediated IaC as file
  const downloadRemediated = () => {
    const blob = new Blob([remediatedIac], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "remediated_iac.tf";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Remediation Suggestions</h2>
      {loading && <div className="text-blue-500 mb-2">Loading suggestions…</div>}
      <ul>
        {suggestions.length === 0 && !loading && (
          <li className="text-gray-500">No remediation suggestions found!</li>
        )}
        {suggestions.map((s) => (
          <li key={s.id} className="mb-2 flex items-center">
            <span
              className={`mr-2 font-semibold ${
                s.priority === "High" ? "text-red-600" : "text-yellow-600"
              }`}
            >
              {s.priority}
            </span>
            <span className="flex-1">{s.text}</span>
            <button
              className="bg-green-600 text-white px-2 rounded mx-1"
              onClick={() => handleAccept(s.suggested_block)}
            >
              Accept
            </button>
            <button
              className="bg-red-600 text-white px-2 rounded mx-1"
              onClick={() => alert("Suggestion rejected.")}
            >
              Reject
            </button>
          </li>
        ))}
      </ul>

      {remediatedIac && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Remediated IaC (Ready to Download):</h3>
          <textarea
            className="w-full h-32 p-2 border rounded"
            value={remediatedIac}
            readOnly
          />
          <button
            onClick={downloadRemediated}
            className="mt-2 bg-blue-700 text-white px-4 py-2 rounded"
          >
            Download Remediated IaC
          </button>
        </div>
      )}
    </div>
  );
}
