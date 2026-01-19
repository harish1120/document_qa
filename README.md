# 📄 PDF Question Answering (RAG)

<div align="center">

![RAG Architecture](https://img.shields.io/badge/RAG-Hybrid%20Search-blue?style=for-the-badge&logo=ai)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53-FF4B4B?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)

*A hybrid search-powered RAG system for intelligent PDF document question answering*

</div>

---

## ✨ Features

- 📚 **PDF Upload** - Upload any PDF document
- 🔍 **Hybrid Search** - Combines dense (FAISS) + sparse (BM25) retrieval
- 🤖 **AI-Powered Answers** - Uses GPT for accurate responses with source citations
- 📊 **Source Attribution** - Shows exactly which pages supported each answer
- 🚀 **Production Ready** - Dockerized with health checks and monitoring

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                       │
│              Streamlit Frontend (:8501)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend (:8000)                 │
│                                                             │
│  ┌─────────────┐    ┌──────────────────┐    ┌───────────┐   │
│  │   Upload    │───▶│   Ingest (PDF)   │───▶│  FAISS +  │   │
│  │   Endpoint  │    │   PyPDFLoader    │    │   BM25    │   │
│  └─────────────┘    └──────────────────┘    └───────────┘   │
│                                                    │        │
│  ┌─────────────┐    ┌──────────────────┐           ▼        │
│  │   Ask       │◀───│   Hybrid Search  │◀───  Vectorstore   │
│  │   Endpoint  │    │   (α = 0.5)      │                    │
│  └─────────────┘    └──────────────────┘                    │
│                            │                                │
│                            ▼                                │
│                   ┌─────────────────┐                       │
│                   │  GPT-5-nano +   │                       │
│                   │  Prompt Engine  │                       │
│                   └─────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   OpenAI API        │
                    │   (Embeddings + LL) │
                    └─────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

### 1. Clone & Setup

```bash
git clone https://github.com/harish1120/document_qa.git
cd document_qa
```

### 2. Configure Environment

Create a `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
```

### 3. Launch with Docker Compose

```bash
docker compose up -d --build
```

### 4. Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:8501 | Streamlit Web UI |
| **Backend** | http://localhost:8000 | FastAPI REST API |
| **Health** | http://localhost:8000/health | Health Check |
| **Metrics** | http://localhost:8000/metrics | Prometheus Metrics |

---

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status":"ok","service":"rag-backend"}
```

### Upload PDF
```bash
curl -X POST http://localhost:8000/upload_pdf \
  -F "file=@document.pdf"
```

### Index Document
```bash
curl -X POST "http://localhost:8000/index?path=data/uploads/doc.pdf"
```

### Ask Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the main topic?"}'
```

---

## 🧪 Hybrid Search Explained

This implementation uses a **Weighted Hybrid Search** combining:

| Search Type | Technique | Strength |
|-------------|-----------|----------|
| **Dense** | FAISS + OpenAI Embeddings | Semantic similarity |
| **Sparse** | BM25 | Keyword matching |

```python
# Balance factor: α = 0.5
final_score = α × (1 - dense_score) + (1 - α) × sparse_score
```

This approach provides more robust retrieval than either method alone.

---

## 📁 Project Structure

```
document_qa/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── rag.py            # Hybrid search & LLM integration
│   ├── ingest.py         # PDF processing & indexing
│   ├── schemas.py        # Pydantic models
│   ├── Dockerfile        # Backend container
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── app.py            # Streamlit UI
│   ├── Dockerfile        # Frontend container
│   └── requirements.txt  # Python dependencies
├── vectorstore/          # Persistent FAISS index
│   ├── index.faiss
│   └── docs.pkl
├── data/
│   └── uploads/          # Uploaded PDFs
├── docker-compose.yml    # Multi-container setup
└── README.md
```

---

## 🔧 Development

### Run Locally (without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Rebuild After Changes

```bash
docker compose up -d --build
```

---

## 📊 Monitoring

Prometheus metrics are available at `/metrics`:
- `http_requests_total` - Request count by handler/method
- `http_request_duration_seconds` - Latency histograms
- `http_request_size_bytes` - Request/response sizes

---

## 🛡️ Security Notes

- 🔐 **API Key**: Store in environment variables, never commit to git
- 🌐 **Production**: Configure AWS Security Groups for your IP only
- 📝 **Logging**: Logs are accessible via `docker logs rag-frontend`

---

## 📝 License

MIT License - Feel free to use and modify!

---

<div align="center">

Made using FastAPI + Streamlit + LangChain + OpenAI

</div>

