# 🛡️ FinAUDIT - AI-Powered Compliance & Health System

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-cyan)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%20Flash-orange)

**FinAUDIT** is an advanced regulatory compliance and data health system designed for financial datasets. It combines deterministic rule engines with Generative AI (Google Gemini) to provide audit-grade analysis, risk assessment, and actionable remediation steps.

---

## 👥 Collaborators

| Name | Role | GitHub |    
|------|------|--------|
| **Anish Ramesh** | Developer | [@Anish-Ramesh](https://github.com/Anish-Ramesh) |
| **Ganesh Arihanth** | Developer | [@GaneshArihanth](https://github.com/GaneshArihanth) |
| **Boopendranath** | Lead Researcher | [@swankystark](https://github.com/swankystark) |
| **Eashwar Kumar** | Lead Tester | [@Eashwar-Kumar-T](https://github.com/Eashwar-Kumar-T) |

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
git clone [https://github.com/Anish-Ramesh/VISA-AI-PROBLEM-STATEMENT-3.git](https://github.com/Anish-Ramesh/VISA-AI-PROBLEM-STATEMENT-3.git)
cd VISA-AI-PROBLEM-STATEMENT-3
