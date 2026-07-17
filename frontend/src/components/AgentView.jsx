import React, { useState } from 'react';
import { Send, DollarSign, Scale, Shield, GitMerge } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function AgentView() {
  const [activeAgent, setActiveAgent] = useState('financial');
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const agents = [
    { id: 'financial', label: 'Financial', icon: DollarSign },
    { id: 'legal', label: 'Legal', icon: Scale },
    { id: 'compliance', label: 'Compliance', icon: Shield },
    { id: 'cross_analysis', label: 'Cross-Analysis', icon: GitMerge },
  ];

  const handleAsk = async () => {
    if (!query.trim()) return;
    
    const userMsg = { role: 'user', content: query };
    setChatHistory([...chatHistory, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/agents/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_type: activeAgent,
          question: userMsg.content
        })
      });
      
      const data = await response.json();
      
      setChatHistory(prev => [...prev, {
        role: 'agent',
        content: data.response,
        sources: data.sources
      }]);
    } catch (error) {
      console.error(error);
      setChatHistory(prev => [...prev, {
        role: 'agent',
        content: 'Error connecting to the backend server. Please try again.',
        sources: []
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="view-content glass-panel" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="view-header">
        <h1>Specialized AI Agents</h1>
        <p>Select a domain expert to interrogate the uploaded documents.</p>
      </div>

      <div className="agent-selector">
        {agents.map(agent => {
          const Icon = agent.icon;
          return (
            <button
              key={agent.id}
              className={`agent-btn ${activeAgent === agent.id ? 'active' : ''}`}
              onClick={() => setActiveAgent(agent.id)}
            >
              <Icon size={24} />
              <span>{agent.label}</span>
            </button>
          )
        })}
      </div>

      <div className="chat-container">
        {chatHistory.length === 0 ? (
          <div style={{ margin: 'auto', color: 'var(--text-secondary)', textAlign: 'center' }}>
            <p>Start a conversation with the {activeAgent} agent.</p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              {msg.role === 'user' ? (
                <p style={{ margin: 0, color: '#fff' }}>{msg.content}</p>
              ) : (
                <div className="markdown-body">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                  {msg.sources && msg.sources.length > 0 && (
                    <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      <strong>Sources:</strong> {msg.sources.join(', ')}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        {loading && (
          <div className="message agent">
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Agent is thinking...</p>
          </div>
        )}
      </div>

      <div className="input-area">
        <input 
          type="text" 
          placeholder={`Ask the ${activeAgent} agent...`} 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
        />
        <button onClick={handleAsk} disabled={loading}>
          <Send size={18} />
          Ask
        </button>
      </div>
    </div>
  );
}
