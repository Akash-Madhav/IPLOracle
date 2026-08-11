# 🏏 IPL Oracle - Execution & Architecture Guide

This document provides a comprehensive, step-by-step guide to set up, configure, index, test, and run both the **Backend** (FastAPI) and **Frontend** (React + Vite + TypeScript) of the **IPL Oracle** system.

---

## 🏗️ Tech Stack Overview

- **Backend**: Python 3.12+ (tested up to 3.14), FastAPI, Uvicorn, SentenceTransformers, Pinecone Vector DB, Google Gemini API, RapidFuzz.
- **Frontend**: Node.js, React 18, TypeScript, Vite, Tailwind CSS, Radix UI, Lucide Icons.

---

## 📋 Prerequisites

Before starting, ensure you have installed:
1. **Python**: 3.12 or higher (`python --version`)
2. **Node.js**: 18.x or higher (`node -v` & `npm -v`)
3. **API Keys**:
   - **Pinecone API Key**: Required for vector database storage and player data retrieval ([Get Pinecone Key](https://www.pinecone.io/)).
   - **Gemini API Key**: Optional, for AI-generated response synthesis ([Get Gemini Key](https://aistudio.google.com/)).

---

## 🚀 Quick Start Guide

Open **two separate terminal windows** (one for the Backend and one for the Frontend).

---

### Step 1: Backend Setup & Execution

#### 1. Navigate to the backend folder
```powershell
cd C:\Users\akash\IPLOracle\backend
```

#### 2. Create and Activate Virtual Environment
```powershell
# Windows PowerShell
py -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Python Dependencies
> ⚠️ **Note**: Backend is written in Python. Do **NOT** run `npm i` in the backend folder.
```powershell
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the `backend/` directory based on `.env.example`:
```powershell
cp .env.example .env
```
Edit `backend/.env` with your actual keys:
```env
PINECONE_API_KEY=your_actual_pinecone_api_key
PINECONE_REGION=us-east-1
PINECONE_CLOUD=aws
INDEX_NAME=ipl-players
GEMINI_API_KEY=your_actual_gemini_api_key
ENV=development
PORT=8000
```

#### 5. Build / Initialize Vector Index (First Time Setup)
To build and populate the vector embeddings in Pinecone from the CSV data:
```powershell
python services/pinecone_build_index.py
```

#### 6. Launch Backend Server
```powershell
uvicorn main:app --reload --port 8000
```
- The backend will start on **`http://localhost:8000`**.
- OpenAPI / Swagger documentation is available at **`http://localhost:8000/docs`**.

---

### Step 2: Frontend Setup & Execution

#### 1. Navigate to the frontend folder
```powershell
cd C:\Users\akash\IPLOracle\frontend
```

#### 2. Install Node Dependencies
```powershell
npm install
```

#### 3. Configure Environment Variables
Create a `.env` file in the `frontend/` directory based on `.env.example`:
```powershell
cp .env.example .env
```
Contents of `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

#### 4. Launch Frontend Development Server
```powershell
npm run dev
```
- The frontend web application will start on **`http://localhost:5173`** (or the URL output by Vite).

---

## 🧪 Verification & Testing

### 1. Verify Backend Health
Open your browser or run in PowerShell:
```powershell
curl http://localhost:8000/health
```
Expected output:
```json
{"status": "healthy", "service": "IPL Insight Bot"}
```

### 2. Run Backend Test Suite
From inside the `backend/` folder with virtual environment activated:
```powershell
# Run basic backend functionality tests
python test_backend.py

# Run integration tests
python test_integration.py

# Run query improvement & superlative ranking tests
python test_query_improvements.py
python test_superlative_queries.py
```

---

## 📁 Environment Variables Summary

| Directory | File | Variable | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `backend/` | `.env` | `PINECONE_API_KEY` | **Yes** | API key for Pinecone vector database |
| `backend/` | `.env` | `PINECONE_REGION` | No | Default `us-east-1` |
| `backend/` | `.env` | `PINECONE_CLOUD` | No | Default `aws` |
| `backend/` | `.env` | `INDEX_NAME` | No | Default `ipl-players` |
| `backend/` | `.env` | `GEMINI_API_KEY` | No | Recommended for AI synthesis |
| `backend/` | `.env` | `PORT` | No | Default `8000` |
| `frontend/`| `.env` | `VITE_API_URL` | **Yes** | Backend URL (`http://localhost:8000`) |

---

## ❓ Common Troubleshooting & Tips

1. **`npm error ENOENT: Could not read package.json` in Backend**:
   - *Cause*: `backend` is a Python/FastAPI project, not a Node project.
   - *Fix*: Use `pip install -r requirements.txt` instead.

2. **`PINECONE_API_KEY is required` Error on Backend Startup**:
   - *Cause*: `.env` file is missing or `PINECONE_API_KEY` is not set.
   - *Fix*: Create `backend/.env` containing a valid `PINECONE_API_KEY`.

3. **CORS Error between Frontend & Backend**:
   - *Cause*: Backend URL mismatch in frontend `.env`.
   - *Fix*: Ensure `VITE_API_URL=http://localhost:8000` in `frontend/.env` and restart the Vite server (`npm run dev`).
