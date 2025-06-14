
// This component allows users to input architecture details in various formats.
// It includes a textarea for pasting logs, YAML, or Terraform code and a submit button.
// The component uses local state to manage the input value and updates it on change.


import React, { useState } from "react";
export default function ArchitectureInput() {
  const [value, setValue] = useState("");
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Architecture Input</h2>
      <textarea
        className="w-full h-40 p-2 border rounded"
        placeholder="Paste logs, YAML, or Terraform here..."
        value={value}
        onChange={e => setValue(e.target.value)}
      />
      <button className="mt-2 bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
    </div>
  );
}

