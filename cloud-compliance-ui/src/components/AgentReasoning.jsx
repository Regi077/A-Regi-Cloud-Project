// =============================================================================
//  AgentReasoning.jsx -- Cloud Compliance Agent Reasoning Trace Component
// =============================================================================
//  Author: Reginald
//
//  DESCRIPTION:
//    - Displays the real-time step-by-step thought process or decision trace from the LLM/agent.
//    - Visually logs each step as a timeline, DeepSeek-style, with time, step type, and description.
//    - Latest step animates with a typing indicator (animated dots).
//    - Also shows the current inputData state at the bottom (used for context/debug).
//    - Accepts reasoningSteps (array) and inputData (object) as props from Dashboard.
// =============================================================================

import React from "react";

// Typing Animation Dots (for last step)
function TypingDots() {
  const [dots, setDots] = React.useState(".");
  React.useEffect(() => {
    const interval = setInterval(() => {
      setDots(dots => (dots.length < 3 ? dots + "." : "."));
    }, 500);
    return () => clearInterval(interval);
  }, []);
  return <span className="ml-1">{dots}</span>;
}

export default function AgentReasoning({ reasoningSteps = [], inputData = {} }) {
  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col items-center">
      <h2 className="font-bold text-xl mb-4">Agent Reasoning Trace</h2>
      <div className="w-full bg-gray-100 rounded p-4 space-y-4 shadow min-h-[200px]">
        {/* If empty, display placeholder */}
        {reasoningSteps.length === 0 && (
          <div className="text-gray-500 text-center">
            No reasoning steps yet. Start by uploading data or performing an action.
          </div>
        )}

        {/* Otherwise, show reasoning timeline */}
        {reasoningSteps.map((step, idx) => (
          <div key={idx} className="flex items-start">
            {/* Step Type (dot and label) */}
            <div className="flex-shrink-0 mr-2 mt-1">
              <span
                className={`w-3 h-3 rounded-full inline-block
                  ${step.step === "Final Verdict"
                    ? "bg-green-500"
                    : step.step === "Error"
                    ? "bg-red-500"
                    : "bg-gray-400"}
                `}
                title={step.step}
              />
            </div>
            <div>
              <div className="font-semibold text-gray-700">
                {step.step || "Step"}
                <span className="ml-2 text-xs text-gray-400">
                  {step.at ? new Date(step.at).toLocaleTimeString() : ""}
                </span>
              </div>
              <div className="text-gray-800">
                {step.desc || step.result || ""}
                {/* Typing animation for last (most recent) step only */}
                {idx === reasoningSteps.length - 1 && <TypingDots />}
              </div>
            </div>
          </div>
        ))}

        {/* Show inputData summary at the bottom, only if not empty */}
        {inputData && Object.keys(inputData).length > 0 && (
          <div className="mt-6 bg-white rounded p-4 shadow text-xs text-gray-700">
            <div className="font-semibold mb-2 text-gray-800">Current Input Data:</div>
            <pre className="overflow-x-auto">{JSON.stringify(inputData, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

// =============================================================================
//  End of AgentReasoning.jsx -- Live, DeepSeek-style agent trace with animation and input state
// =============================================================================
