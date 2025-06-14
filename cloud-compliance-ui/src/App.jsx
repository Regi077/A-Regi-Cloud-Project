

// This is the main App component that conditionally renders either the Login
//   or Dashboard component based on the user's authentication state.
// It uses React's useState hook to manage the user state, and passes the onLogin and onLogout callbacks to handle user authentication.
// The Login component is responsible for rendering the login form and handling user credentials, while the Dashboard component displays the main application interface once the user is logged in.



import React, { useState } from "react";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";

export default function App() {
  const [user, setUser] = useState(null);
  return user ? <Dashboard user={user} onLogout={() => setUser(null)} /> : <Login onLogin={setUser} />;
}

