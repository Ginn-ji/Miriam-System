import "@/App.css";
import React, { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { LanguageProvider } from "./contexts/LanguageContext";
import { Sidebar } from "./components/Sidebar";
import { Dashboard } from "./components/Dashboard";
import { LegalChat } from "./components/LegalChat";
import { History } from "./components/History";
import { Knowledge } from "./components/Knowledge";
import Login from "./components/Login";
import { Toaster } from "./components/ui/sonner";

function App() {
  const [user, setUser] = useState(null);

  // If user is not authenticated, strictly show the Login/Register component
  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <LanguageProvider>
      <div className="App flex h-screen overflow-hidden bg-background">
        <BrowserRouter>
          {/* Sidebar now receives the logged-in user and a logout function */}
          <Sidebar user={user} onLogout={() => setUser(null)} />
          <main className="flex-1 overflow-y-auto p-8">
            <Routes>
              <Route path="/" element={<Dashboard user={user} />} />
              <Route path="/chat" element={<LegalChat user={user} />} />
              {/* History is only accessible if user is not a guest */}
              <Route 
                path="/history" 
                element={user.role !== 'guest' ? <History user={user} /> : <Navigate to="/chat" />} 
              />
              <Route 
                path="/knowledge" 
                element={user.role === 'admin' ? <Knowledge user={user} /> : <Navigate to="/chat" />} 
              />
            </Routes>
          </main>
        </BrowserRouter>
        <Toaster position="top-right" />
      </div>
    </LanguageProvider>
  );
}

export default App;