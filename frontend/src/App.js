import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LanguageProvider } from "./contexts/LanguageContext";
import { Sidebar } from "./components/Sidebar";
import { Dashboard } from "./components/Dashboard";
import { Documents } from "./components/Documents";
import { Translate } from "./components/Translate";
import { LegalChat } from "./components/LegalChat";
import { History } from "./components/History";
import { Knowledge } from "./components/Knowledge";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <LanguageProvider>
      <div className="App flex h-screen overflow-hidden bg-background">
        <BrowserRouter>
          <Sidebar />
          <main className="flex-1 overflow-y-auto p-8" data-testid="main-content">
            <div className="max-w-7xl mx-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/documents" element={<Documents />} />
                <Route path="/translate" element={<Translate />} />
                <Route path="/chat" element={<LegalChat />} />
                <Route path="/history" element={<History />} />
                <Route path="/knowledge" element={<Knowledge />} />
              </Routes>
            </div>
          </main>
        </BrowserRouter>
        <Toaster position="top-right" />
      </div>
    </LanguageProvider>
  );
}

export default App;