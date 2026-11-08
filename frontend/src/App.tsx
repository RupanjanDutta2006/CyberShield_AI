import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { Scanner } from './pages/Scanner';
import { MessageAnalyzer } from './pages/MessageAnalyzer';
import { History } from './pages/History';
import { ReportDetail } from './pages/ReportDetail';
import { Settings } from './pages/Settings';
import { ParticleExperience } from './components/experience/ParticleExperience';
import { Shield } from 'lucide-react';

const AppContent: React.FC = () => {
  const location = useLocation();
  const isExperience = location.pathname === '/' || location.pathname === '/experience';

  if (isExperience) {
    return (
      <Routes>
        <Route path="/" element={<ParticleExperience />} />
        <Route path="/experience" element={<ParticleExperience />} />
      </Routes>
    );
  }

  return (
    <div className="min-h-screen bg-[#000000] text-slate-100 flex flex-col font-['Plus_Jakarta_Sans',sans-serif]">
      <Navbar />

      <main className="flex-grow">
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/scanner" element={<Scanner />} />
          <Route path="/message-analyzer" element={<MessageAnalyzer />} />
          <Route path="/history" element={<History />} />
          <Route path="/report/:id" element={<ReportDetail />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>

      <footer className="border-t border-[#1C1C1C] bg-black py-6 mt-12 text-xs text-[#8A8A8A] font-mono">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-[#AA88FF]" />
            <span className="font-semibold text-[#DDDDDD]">CyberShield AI Platform</span>
            <span>&bull;</span>
            <span>Digital Threat Intelligence &bull; 2026</span>
          </div>
          <p className="text-center sm:text-right text-[11px] text-[#8A8A8A] max-w-md">
            Disclaimer: Threat intelligence scores are probabilistic. Always correlate findings with internal SIEM and perimeter defenses before taking operational actions.
          </p>
        </div>
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
