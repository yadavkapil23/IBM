import React, { useState } from 'react';
import { Activity, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function ReportView() {
  const [riskData, setRiskData] = useState(null);
  const [reportText, setReportText] = useState(null);
  const [loadingScore, setLoadingScore] = useState(false);
  const [loadingReport, setLoadingReport] = useState(false);

  const handleGenerateScore = async () => {
    setLoadingScore(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/agents/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_type: 'risk_scoring',
          question: 'Calculate the overall risk score based on all available documents.'
        })
      });
      const data = await response.json();
      setRiskData(data.response); // The response is parsed JSON from the backend
    } catch (error) {
      console.error(error);
      alert('Error fetching risk score.');
    } finally {
      setLoadingScore(false);
    }
  };

  const handleGenerateReport = async () => {
    setLoadingReport(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/agents/report', {
        method: 'POST'
      });
      const data = await response.json();
      setReportText(data.report);
    } catch (error) {
      console.error(error);
      alert('Error generating executive report.');
    } finally {
      setLoadingReport(false);
    }
  };

  return (
    <div className="view-content" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div className="view-header">
        <h1>Executive Dashboard</h1>
        <p>Review the comprehensive Risk Score and generate the final Executive Summary Report.</p>
      </div>

      <div className="report-actions">
        <button className="secondary" onClick={handleGenerateScore} disabled={loadingScore}>
          <Activity size={18} />
          {loadingScore ? 'Calculating Score...' : 'Calculate Overall Risk Score'}
        </button>
        <button className="secondary" onClick={handleGenerateReport} disabled={loadingReport}>
          <FileText size={18} />
          {loadingReport ? 'Generating Report...' : 'Generate Executive Report'}
        </button>
      </div>

      {riskData && (
        <div className={`glass-panel score-card ${riskData.risk_level}`}>
          <h3>Due Diligence Risk Score</h3>
          <div className="score-value">{riskData.score} / 100</div>
          <h4 style={{ margin: '1rem 0' }}>Risk Level: {riskData.risk_level}</h4>
          
          <div style={{ textAlign: 'left', marginTop: '1.5rem', background: 'rgba(0,0,0,0.2)', padding: '1.5rem', borderRadius: '12px' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Primary Reasons</h4>
            <ul style={{ margin: 0, paddingLeft: '1.5rem', color: 'var(--text-secondary)' }}>
              {riskData.reasons && riskData.reasons.map((r, i) => (
                <li key={i} style={{ marginBottom: '0.5rem' }}>{r}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {reportText && (
        <div className="glass-panel markdown-container markdown-body">
          <ReactMarkdown>{reportText}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
