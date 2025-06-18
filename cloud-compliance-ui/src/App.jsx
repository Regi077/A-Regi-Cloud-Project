// =============================================================================
//  App.jsx  --  Main Application Entrypoint (Conditional Routing)
// =============================================================================
//  Author: Reginald
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - This file controls global authentication state for the Cloud Compliance UI.
//    - Depending on user login status, it conditionally renders either the
//      Login screen or the main Dashboard.
//    - Uses React state to track user credentials and session context.
//
//  HOW IT WORKS:
//    - On startup, displays <Login />; after valid credentials, shows <Dashboard />.
//    - User can log out at any time to return to the login form.
//    - Passes onLogin and onLogout handlers as props for modularity.
// =============================================================================

import React, { useState } from "react";
import Login from "./pages/Login.jsx";         // User login form (RBAC, credential check)
import Dashboard from "./pages/Dashboard.jsx"; // Main app UI (all panels/tabs)

// =============================================================================
//  Main App Component
// =============================================================================
export default function App() {
  // Holds current user object; null if not authenticated
  const [user, setUser] = useState(null);

  // If user is logged in, render the Dashboard and pass logout handler.
  // Otherwise, show the Login form and pass login handler.
  return user
    ? <Dashboard user={user} onLogout={() => setUser(null)} />
    : <Login onLogin={setUser} />;
}

// =============================================================================
//  End of App.jsx -- Onboarding-ready main UI entrypoint
// =============================================================================
