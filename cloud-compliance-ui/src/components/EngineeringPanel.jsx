

// This component displays a list of remediation suggestions with options to accept or reject each suggestion.
// It uses a simple array of suggestions with priority levels and renders them in a list.
// Each suggestion has a priority label, text, and buttons for accepting or rejecting the suggestion.
// The component uses Tailwind CSS classes for styling, ensuring a consistent look and feel.



import React from "react";
const suggestions = [
  { id: 1, text: "Enforce MFA on IAM roles", priority: "High" },
  { id: 2, text: "Restrict public S3 buckets", priority: "Medium" },
];
export default function EngineeringPanel() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-4">Remediation Suggestions</h2>
      <ul>
        {suggestions.map(s => (
          <li key={s.id} className="mb-2 flex items-center">
            <span className={`mr-2 font-semibold text-${s.priority==="High"?"red":"yellow"}-600`}>{s.priority}</span>
            <span className="flex-1">{s.text}</span>
            <button className="bg-green-600 text-white px-2 rounded mx-1">Accept</button>
            <button className="bg-red-600 text-white px-2 rounded mx-1">Reject</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

