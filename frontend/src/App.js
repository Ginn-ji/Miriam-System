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
import { Menu, X, LogOut } from "lucide-react"; // <-- Added icons for mobile

function AppContent() {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('shield_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  // --- NEW: Mobile Menu State ---
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigate = useNavigate();
  
  const handleLogin = (userData) => {
    localStorage.setItem('shield_user', JSON.stringify(userData));
    setUser(userData);
    navigate("/"); 
  };

  const handleLogout = () => {
    localStorage.removeItem('shield_user');
    setUser(null);
    setIsMobileMenuOpen(false);
    navigate("/");
  };

  // Closes the menu when a link is clicked or the backdrop is tapped
  const closeMobileMenu = () => setIsMobileMenuOpen(false);

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    // Changed flex-row for desktop, flex-col for mobile
    <div className="App flex flex-col md:flex-row h-screen overflow-hidden bg-background relative">
      
      {/* ==================== MOBILE HEADER ==================== */}
      <div className="md:hidden flex items-center justify-between bg-primary text-white p-4 shadow-md z-40 shrink-0">
        <div className="flex items-center gap-3">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-1 focus:outline-none">
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <h1 className="font-serif font-bold text-xl tracking-wide">LACBot</h1>
        </div>
        {/* Quick logout button for trapped mobile users */}
        <button onClick={handleLogout} className="flex items-center gap-1 text-xs bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-sm transition-colors">
          <LogOut size={16} /> Logout
        </button>
      </div>

      {/* ==================== SIDEBAR WRAPPER ==================== */}
      {/* Handles both desktop static sidebar and mobile slide-out behavior */}
      <div 
        className={`
          absolute md:relative z-50 h-full md:h-auto bg-white shadow-2xl md:shadow-none transition-transform duration-300 ease-in-out
          ${isMobileMenuOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
        `}
        onClick={closeMobileMenu} 
      >
        <Sidebar user={user} onLogout={handleLogout} />
      </div>

      {/* Mobile Dark Backdrop Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="absolute inset-0 bg-black/50 z-40 md:hidden"
          onClick={closeMobileMenu}
        />
      )}

      {/* ==================== MAIN CONTENT ==================== */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 bg-slate-50 relative z-0">
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