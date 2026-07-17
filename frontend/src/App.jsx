import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import UploadView from './components/UploadView';
import AgentView from './components/AgentView';
import ReportView from './components/ReportView';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState('dashboard');

  return (
    <div className="app-container">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      
      <main className="main-content">
        {activeView === 'dashboard' && (
          <div className="view-content glass-panel" style={{ padding: '3rem', textAlign: 'center', marginTop: '10%' }}>
            <h1 style={{ fontSize: '3rem', marginBottom: '1rem', background: 'linear-gradient(135deg, #818cf8, #c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Welcome to AI Due Diligence
            </h1>
            <p style={{ fontSize: '1.25rem', maxWidth: '600px', margin: '0 auto 2rem' }}>
              Automate your M&A audits with specialized AI agents. Upload your documents to begin the analysis.
            </p>
            <button onClick={() => setActiveView('upload')} style={{ fontSize: '1.1rem', padding: '1rem 2rem' }}>
              Get Started
            </button>
          </div>
        )}
        
        {activeView === 'upload' && <UploadView />}
        {activeView === 'agents' && <AgentView />}
        {activeView === 'report' && <ReportView />}
      </main>
    </div>
  );
}

export default App;
