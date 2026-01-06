# 🛡️ FinAUDIT - AI-Powered Compliance & Health System

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-cyan)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%20Flash-orange)

**FinAUDIT** is an advanced regulatory compliance and data health system designed for financial datasets. It combines deterministic rule engines with Generative AI (Google Gemini) to provide audit-grade analysis, risk assessment, and actionable remediation steps.

---

## 🚀 Key Features

### 1. 🌍 Multi-Regulation Compliance Engine
Switch instantly between global standards to re-evaluate your dataset:
- **GDPR**: Data minimization, purpose limitation, and PII checks.
- **Visa CEDP**: Cardholder data security and ecosystem protection.
- **AML / FATF**: Anti-Money Laundering checks (KYC, Source of Funds).
- **PCI DSS**: Payment Card Industry security and storage rules.
- **Basel II / III**: Financial risk data aggregation and reporting.
- **General Transaction**: Baseline data quality and hygiene checks.

### 2. 🤖 Independent AI Auditor
- **Context-Aware Analysis**: The AI adapts its persona based on the selected standard (e.g., acts as a Privacy Officer for GDPR, Risk Manager for Basel).
- **Strategic Recommendations**: prioritizes fixes (CRITICAL / HIGH / MEDIUM / LOW).
- **Dynamic Chat**: Ask "Why did Rule X fail?" or "How do I fix the KYC gaps?" via the built-in Compliance Assistant.

### 3. 📊 Deterministic Data Quality Scoring
- **6-Dimension Scoring**: Completeness, Validity, Accuracy, Uniqueness, Consistency, Timeliness.
- **30+ Hard Rules**: Specific checks for negative amounts, impossible dates, schema drift, null clusters, and more.
- **Privacy-First**: Analysis is performed on **Metadata Only**. Raw PII never leaves your secure environment.

### 4. 📝 Audit Reporting
- **PDF Export**: Generate professional "Independent Auditor's Reports" with hash-signed provenance.
- **Attestation**: Cryptographic fingerprinting of the analysis for audit trails.

---

## 🛠️ Architecture

- **Backend**: FastAPI (Python), Pandas (Profiling), LangGraph (Agentic AI Workflow).
- **Frontend**: React + Vite (Dashboard), Recharts (Visualization), Vanilla CSS (Premium UI).
- **AI Model**: Google Gemini 1.5 Flash (via LangChain).
- **Deployment**: Docker-ready, optimized for Render.com.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- Google API Key (for AI features)

### 1. Clone & Setup
```bash
git clone https://github.com/Anish-Ramesh/VISA-AI-PROBLEM-STATEMENT-3.git
cd VISA-AI-PROBLEM-STATEMENT-3
```

### 2. Run Locally (One-Shot)
We provide a `build.sh` script to set up everything:
```bash
# Windows (Git Bash) or Linux/Mac
./build.sh
```

### 3. Run Manually
**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
pip install -r requirements.txt
# Create .env file with GOOGLE_API_KEY=your_key
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** (Frontend) or **http://localhost:8000** (Full Stack if built).

---

## ☁️ Deployment (Render)

This project is configured for seamless deployment on **Render.com**.

1. **Connect Repository**: Link this repo to Render.
2. **Settings**:
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   - `PYTHON_VERSION`: `3.11.0`
   - `NODE_VERSION`: `18.17.0`
   - `GOOGLE_API_KEY`: `...`
4. **Deploy**: Render will auto-build the React frontend and serve it via FastAPI from `backend/static`.

---

## 🔒 Security Summary
- **No Data Retention**: Uploaded files are processed in-memory and discarded.
- **Metadata Analyzed**: The AI only sees statistical summaries (column names, null counts), not raw rows.
- **PII Guardrails**: Automatic redaction of sensitive columns before processing.

---

## 📜 License
MIT License. Created by Anish Ramesh, 2024.
