// =============================================================================
//  login.jsx -- User Login Form for Cloud Compliance UI
// =============================================================================
//  Author: Reginald
//  Last updated: 18th June 2025
//
//  DESCRIPTION:
//    - Provides a secure login interface for users (Admin, Service Provider, Client).
//    - Validates credentials against a local static list (see utils/rbac.js).
//    - Calls onLogin(userObj) with the user object if credentials are correct.
//    - Shows user-friendly error if login fails.
//
//  KEY UX FEATURES:
//    - Username/password fields, styled with Tailwind for clean, modern UI.
//    - Error feedback for wrong credentials.
//    - Demo credentials for all roles displayed for easy onboarding/testing.
//
//  HOW TO EXTEND:
//    - To use real backend auth, swap the user list for an API call.
//    - To add more roles/users, update users array in utils/rbac.js.
// =============================================================================

import React, { useState } from "react";
import { users } from "../utils/rbac";   // Static list of user objects for demo

export default function Login({ onLogin }) {
  const [username, setUsername] = useState(""); // Username input field
  const [password, setPassword] = useState(""); // Password input field
  const [err, setErr] = useState("");           // Error message for invalid login

  // Handle form submission (login attempt)
  function handleSubmit(e) {
    e.preventDefault();
    // Find matching user (case-sensitive)
    const found = users.find(
      u => u.username === username && u.password === password
    );
    if (found) {
      onLogin(found);     // Successful login, pass user object up
    } else {
      setErr("Invalid credentials"); // Show error if not found
    }
  }

  // -------------------------- RENDER LOGIN FORM -----------------------------
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6">Cloud Compliance Tool Login</h2>
        <input
          className="block w-full p-2 mb-4 border rounded"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          className="block w-full p-2 mb-4 border rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        {err && <p className="text-red-500">{err}</p>}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
        >
          Login
        </button>

        {/* Demo credentials for onboarding/testing (remove in production!) */}
        <div className="mt-3 text-xs text-gray-400">
          <p><b>Admin</b>: Reginald / hart12345</p>
          <p><b>Service Provider</b>: AD-Astra / AD12345</p>
          <p><b>Client</b>: SkyLock / Lock12345</p>
        </div>
      </form>
    </div>
  );
}

// =============================================================================
//  End of login.jsx -- Secure, onboarding-friendly login UI
// =============================================================================
