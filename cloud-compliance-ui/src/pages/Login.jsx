import React, { useState } from "react";
import { users } from "../utils/rbac";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const found = users.find(u => u.username === username && u.password === password);
    if (found) {
      onLogin(found);
    } else {
      setErr("Invalid credentials");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6">Cloud Compliance Tool Login</h2>
        <input className="block w-full p-2 mb-4 border rounded"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)} />
        <input className="block w-full p-2 mb-4 border rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)} />
        {err && <p className="text-red-500">{err}</p>}
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Login</button>
        
        
        <div className="mt-3 text-xs text-gray-400">


          <p><b>Admin</b>: Reginald / hart12345</p>
          <p><b>ServiceProvider</b>: AD-Astra / AD12345</p>
          <p><b>Client</b>: SkyLock / Lock12345</p>
        </div>
      </form>
    </div>
  );
}


// This component handles user login, validates credentials against a predefined list,
// and calls the onLogin callback with the user object if successful.
// It also displays a simple login form with username and password fields, and shows an error message if the credentials are invalid.
// The component is styled using Tailwind CSS classes for a clean and modern look.  

