import "@/App.css";
import React, { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { LanguageProvider } from "./contexts/LanguageContext";
import { Sidebar } from "./components/Sidebar";
import { Dashboard } from "./components/Dashboard";
import { LegalChat } from "./components/LegalChat";
import { History } from "./components/History";
import { Knowledge } from "./components/Knowledge";
import Login from "./components/Login";
import { Toaster } from "./components/ui/sonner";

function AppContent() {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('shield_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const navigate = useNavigate();
  const handleLogin = (userData) => {
    localStorage.setItem('shield_user', JSON.stringify(userData));
    setUser(userData);
    navigate("/"); 
  };

  const handleLogout = () => {
    localStorage.removeItem('shield_user');
    setUser(null);
    navigate("/");
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App flex h-screen overflow-hidden bg-background">
      <Sidebar user={user} onLogout={handleLogout} />
      <main className="flex-1 overflow-y-auto p-8">
        <Routes>
          <Route path="/" element={<Dashboard user={user} />} />
          <Route path="/chat" element={<LegalChat user={user} />} />
          <Route 
            path="/history" 
            element={user.role !== 'guest' ? <History user={user} /> : <Navigate to="/chat" />} 
          />
          <Route path="/knowledge" element={<Knowledge user={user} />} />
          
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  );
}

// THE WRAPPER
function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <AppContent />
        <Toaster position="top-right" />
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;