// =============================================================================
//  EngineeringPanel.jsx -- Remediation Suggestion UI for Azure Cloud Compliance
// =============================================================================
//  Author: Reginald
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Fetches remediation suggestions from the backend IaC analysis microservice.
//    - Lets users Accept/Reject individual suggestions, and downloads remediated IaC.
//    - Designed for idiot-proof, executive-grade usability with clear code comments.
//
//  KEY FEATURES:
//    - Fetches remediation advice based on sample IaC for Azure.
//    - Each suggestion is labeled by priority and has Accept/Reject actions.
//    - Accept: appends the recommended block to the original IaC for download.
//    - Download button lets users export the updated, compliant IaC.
//    - Dummy content is used for demo; integrate with real context/state in production.
//    - Tailwind CSS for modern, accessible styling.
// =============================================================================

import React, { useEffect, useState } from "react";

export default function EngineeringPanel() {
  // State for suggestions from backend, user IaC, and the remediated result
  const [suggestions, setSuggestions] = useState([]);
  const [iacContent, setIacContent] = useState(""); 
  const [remediatedIac, setRemediatedIac] = useState("");
  const [loading, setLoading] = useState(false);

  // On mount, populate IaC sample (replace with real input in live system)
  useEffect(() => {
    setIacContent(
      'resource "azurerm_storage_account" "example" {\n  name = "mystorageaccount"\n  location = "eastus"\n}'
    );
  }, []);

  // Fetch remediation suggestions whenever IaC content changes
  useEffect(() => {
    setLoading(true);
    fetch("http://localhost:5030/analyze-iac", {
      method: "POST",
      body: (() => {
        const fd = new FormData();
        const blob = new Blob([iacContent], { type: "text/plain" });
        fd.append("iac", blob, "iac.tf");
        fd.append("framework", "Azure");
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

  // Handle Accept: append block to IaC
  const handleAccept = (block) => {
    const updated = iacContent + "\n\n" + block;
    setRemediatedIac(updated);
    alert("Remediation block appended! Download below.");
  };

  // Download remediated IaC as .tf file
  const downloadRemediated = () => {
    const blob = new Blob([remediatedIac], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "remediated_iac.tf";
    a.click();
    URL.revokeObjectURL(url);
  };

  // =============================================================================
  //  Main UI: Display suggestions and actions, show remediated IaC for download
  // =============================================================================

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

// =============================================================================
//  End of EngineeringPanel.jsx -- Hassle-free, idiot-proof remediation panel UI
// =============================================================================
