import React from 'react';
import { Home, UploadCloud, Users, FileText } from 'lucide-react';

export default function Sidebar({ activeView, setActiveView }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'upload', label: 'Upload Documents', icon: UploadCloud },
    { id: 'agents', label: 'AI Agents', icon: Users },
    { id: 'report', label: 'Executive Report', icon: FileText },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>AI Due Diligence</h2>
      </div>
      
      <nav className="nav-links">
        {navItems.map(item => {
          const Icon = item.icon;
          return (
            <a 
              key={item.id}
              className={`nav-link ${activeView === item.id ? 'active' : ''}`}
              onClick={(e) => { e.preventDefault(); setActiveView(item.id); }}
            >
              <Icon size={20} />
              {item.label}
            </a>
          );
        })}
      </nav>
    </div>
  );
}
