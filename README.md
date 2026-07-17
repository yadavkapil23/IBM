# AI-Powered Due Diligence Platform

An intelligent, AI-powered system designed to automate the manual due diligence process when acquiring or auditing a company. Instead of spending weeks reading hundreds of financial, legal, and compliance documents, this platform uses state-of-the-art AI to parse, analyze, and generate comprehensive risk reports instantly.

## 🚀 Features

- **Multi-Format Document Ingestion**: Supports uploading PDFs, Word documents (`.docx`), and Excel spreadsheets (`.xlsx`).
- **Retrieval-Augmented Generation (RAG)**: Automatically chunks, embeds, and indexes documents into a local vector database for rapid similarity search.
- **Cross-Document Reasoning**: Detects inconsistencies across different types of documents (e.g., mismatching employee counts between HR reports and financial balance sheets).
- **Specialized AI Agents (Planned)**: Financial, Legal, Compliance, and Risk agents to assess different aspects of the uploaded documents.
- **Risk Scoring (Planned)**: Automatically calculates an overall due diligence risk score and recommendation.

## 🏗️ Architecture & Tech Stack

- **Frontend**: React + Vite + Vanilla CSS (for dynamic, premium UI aesthetics).
- **Backend**: Python + FastAPI (for high-performance, asynchronous endpoints).
- **Vector Database**: ChromaDB (local persistence).
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`) via `sentence-transformers`.
- **LLM Integration**: LangChain (orchestration) + NVIDIA AI Endpoints (Llama 3/Mistral).

## ⚙️ Prerequisites

- **Python 3.10+**
- **Node.js 18+**

## 🛠️ Setup & Installation

### 1. Clone the repository
Navigate to the project root directory.

### 2. Backend Setup
```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Start the Backend Server
From the `backend` directory, with your virtual environment activated:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API documentation (Swagger UI) will be available at: http://localhost:8000/docs

### Start the Frontend Server
From the `frontend` directory:
```bash
npm run dev
```

## 🗺️ Roadmap

- [x] **Phase 1**: Document Ingestion (FastAPI Upload endpoints)
- [x] **Phase 2**: Document Processing (Parsing architecture)
- [x] **Phase 3**: RAG Pipeline (ChromaDB + LangChain embeddings)
- [x] **Phase 4**: Specialized AI Agents (Financial, Legal, Compliance)
- [x] **Phase 5**: Cross-Document Analysis
- [ ] **Phase 6**: Risk Scoring Engine
- [ ] **Phase 7**: Executive Report Generation
- [ ] **Phase 8**: Dashboard UI Construction
- [ ] **Phase 9**: Deployment (Docker, AWS/Azure, PostgreSQL)
