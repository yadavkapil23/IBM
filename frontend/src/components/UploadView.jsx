import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertTriangle } from 'lucide-react';

export default function UploadView() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileChange = (e) => {
    setFiles([...e.target.files]);
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    
    setUploading(true);
    setStatusMessage('Uploading and parsing documents...');
    
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/api/v1/upload/', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      if (response.ok) {
        setStatusMessage(`Successfully processed ${data.results.length} documents!`);
        setFiles([]);
      } else {
        setStatusMessage('Error uploading documents.');
      }
    } catch (error) {
      console.error(error);
      setStatusMessage('Network error occurred.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="view-content glass-panel" style={{ padding: '2rem' }}>
      <div className="view-header">
        <h1>Document Ingestion</h1>
        <p>Upload financial statements, legal contracts, or HR policies.</p>
      </div>

      <div className="upload-dropzone" onClick={() => document.getElementById('file-upload').click()}>
        <Upload size={48} className="upload-icon" />
        <h3>Click to browse or drag & drop files here</h3>
        <p>Supports .pdf, .docx, .xlsx</p>
        <input 
          type="file" 
          id="file-upload" 
          multiple 
          style={{ display: 'none' }} 
          onChange={handleFileChange}
        />
      </div>

      {files.length > 0 && (
        <div className="file-list">
          <h4>Selected Files ({files.length})</h4>
          {files.map((file, idx) => (
            <div key={idx} className="file-item">
              <div className="file-info">
                <FileText size={20} />
                <span>{file.name}</span>
              </div>
              <span style={{color: 'var(--text-secondary)'}}>
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </span>
            </div>
          ))}
          
          <button 
            onClick={handleUpload} 
            disabled={uploading}
            style={{ marginTop: '1rem' }}
          >
            {uploading ? 'Processing...' : 'Upload & Process Documents'}
          </button>
        </div>
      )}

      {statusMessage && (
        <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {statusMessage.includes('Success') ? <CheckCircle color="var(--success-color)" /> : <AlertTriangle color="var(--warning-color)" />}
          <span>{statusMessage}</span>
        </div>
      )}
    </div>
  );
}
