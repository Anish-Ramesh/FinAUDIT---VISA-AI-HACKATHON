# FinAUDIT: The Ultimate Financial Compliance & Health System 🚀

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Backend-FastAPI-green)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash%20%2B%20LangGraph-orange)
![Security](https://img.shields.io/badge/Security-Metadata%20Only-red)
![Deployment](https://img.shields.io/badge/Deployment-Docker%20Ready-blueviolet)

> **"Your Intelligent, Privacy-First Financial Auditor"**

Welcome to **FinAUDIT**! This project is an enterprise-grade AI audit platform designed to validate financial datasets against rigorous global standards like **GDPR**, **PCI DSS**, and **Basel III**.

What makes it special? It does all this **without ever exposing your sensitive raw data**. By combining rigid mathematical rules with the reasoning power of Google's Gemini AI, FinAUDIT delivers professional "Independent Auditor's Reports" that are cryptographically signed for absolute trust.

---

## 📑 Table of Contents

1.  [🌟 Why FinAUDIT Exists](#-why-finaudit-exists)
2.  [🚀 Key Features & Capabilities](#-key-features--capabilities)
3.  [🏗️ System Architecture (How it Works)](#-system-architecture-how-it-works)
4.  [📂 Project Directory Structure](#-project-directory-structure)
5.  [⚡ Installation Guide (Beginner Friendly)](#-installation-guide-beginner-friendly)
    - [Prerequisites](#prerequisites)
    - [Option A: The Automatic Way](#option-a-the-automatic-way)
    - [Option B: The Manual Way](#option-b-the-manual-way)
6.  [🎮 User Manual: How to Use](#-user-manual-how-to-use)
7.  [👨‍💻 Developer Guide: Extending the System](#-developer-guide-extending-the-system)
8.  [🔗 API Documentation](#-api-documentation)
9.  [📖 Glossary of Terms](#-glossary-of-terms)
10. [❓ Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 🌟 Why FinAUDIT Exists

In the modern financial world, data is a liability. Storing credit card numbers (PCI DSS) or personal user data (GDPR) incorrectly can lead to massive fines.

**The Problem:**

- **Manual Audits are Slow**: Humans take weeks to check Excel sheets.
- **AI is Risky**: You can't just upload customer data to ChatGPT/Gemini because of privacy laws.
- **Rules are Rigid**: A simple "if/else" script can't tell you _why_ a transaction looks suspicious, only that it _is_.

**The FinAUDIT Solution:**
We built a bridge. We extract **Statistical Metadata** (min, max, null counts) from your data locally. We send _only_ that safe metadata to the AI. The AI acts as a consultant, explaining compliance gaps without ever seeing a single real name or credit card number.

---

## 🚀 Key Features & Capabilities

### 1. 🛡️ Absolute Privacy (Metadata-Only Analysis)

- **Guardian Layer**: Before data leaves your browser/server, we strip all PII (Personally Identifiable Information).
- **Statistical View**: The AI knows "User_Names column is 50% empty", but it doesn't know who the users are.

### 2. 🧠 Hybrid Intelligence Engine

- **Deterministic Rules**: 30+ hard-coded Python checks for binary pass/fail (e.g., "Is date format ISO8601?").
- **Probabilistic AI**: An LLM (Large Language Model) that reasons about the _results_ of those rules (e.g., "A low date validity score combined with high transaction volume suggests a legacy system migration issue").

### 3. 📊 Data Quality Scoring (DQS)

We grade your data on a strict 0-100 scale across 7 dimensions:

- **Completeness**: Are there meaningful gaps?
- **Validity**: Does the data look like what it claims to be?
- **Accuracy**: Are numerical values consistent?
- **Consistency**: Do related fields match?
- **Timeliness**: Is the data fresh?
- **Integrity**: Are relationships preserved?
- **Security**: Is sensitive data properly masked?

### 4. 📝 Cryptographic Provenance

- **Digital Fingerprinting**: We create a SHA-256 hash of your report.
- **Tamper Proof**: If anyone edits the PDF report later, the hash won't match, proving it's fake.

---

## 🏗️ System Architecture (How it Works)

Understanding the flow of data is key to trusting the system.

1.  **User Upload**: You drag & drop a CSV file into the React Frontend.
2.  **Ingestion Layer (`backend/services/ingestion.py`)**:
    - Pandas reads the file.
    - PII Guardrail scans for sensitive columns headers (e.g., "SSN", "CVV").
    - **Action**: Profiling generates a JSON summary (Metadata). Original file is discarded from memory.
3.  **Rules Engine (`backend/core/rules_engine.py`)**:
    - The Metadata is passed through 30+ Python functions.
    - Result: A big list of `PASS` or `FAIL` booleans.
4.  **Scoring Service (`backend/services/scoring.py`)**:
    - Aggregates passes/fails into weighted scores (0-100).
5.  **AI Analyst (`backend/ai/agent.py`)**:
    - LangGraph constructs a prompt: _"Here is the profile of a financial dataset. It failed the Negative Transaction Rule. Explain why this is bad under Basel III standards."_
    - Gemini 1.5 Flash returns a professional executive summary.
6.  **Report Generation**:
    - Frontend receives the Analysis JSON.
    - `jspdf` builds a pixel-perfect PDF report.

---

## 📂 Project Directory Structure

```text
FinAUDIT/
├── build.sh                 # One-click setup script
├── README.md                # The master guide (You are here!)
├── backend/                 # 🐍 Python FastAPI Server
│   ├── main.py              # Entry point (App initialization)
│   ├── .env                 # Secrets (API Keys) - Create this!
│   ├── requirements.txt     # List of Python libraries
│   ├── ai/                  # 🤖 AI Logic
│   │   └── agent.py         # Talk to Gemini
│   ├── core/                # 📏 Analysis Logic
│   │   └── rules_engine.py  # The math rules (GDPR, PCI logic)
│   ├── services/            # 🛠 Helper Services
│   │   ├── ingestion.py     # Data reading
│   │   └── scoring.py       # Score calculation
│   └── api/                 # 🌐 Web Endpoints
│       └── endpoints.py     # Route definitions
│
└── frontend/                # ⚛️ React Application
    ├── package.json         # Node dependencies
    ├── vite.config.js       # Build configuration
    └── src/
        ├── App.jsx          # Main application wrapper
        ├── components/      # UI Building Blocks
        │   ├── Upload.jsx   # Drag & Drop area
        │   └── ChatAssistant.jsx # AI Chat window
        └── utils/
            └── reportGenerator.js # PDF creation logic
```

---

## ⚡ Installation Guide (Beginner Friendly)

### Prerequisites

Before we start, verify you have these tools:

1.  **Python (3.10 or newer)**: Type `python --version` in your terminal.
2.  **Node.js (16 or newer)**: Type `node -v`.
3.  **Git**: To download the code.
4.  **Google API Key**: Needed for the AI. [Get a free key here](https://aistudio.google.com/app/apikey).

### Option A: The Automatic Way 🪄

_(Best for Mac/Linux users)_

1.  Open your terminal.
2.  Navigate to the project folder.
3.  Run:
    ```bash
    ./build.sh
    ```
4.  Follow the on-screen prompts.

### Option B: The Manual Way 🛠️

_(Best for Windows users or manual control)_

#### Step 1: Clone the Repo

```bash
git clone https://github.com/Anish-Ramesh/VISA-AI-PROBLEM-STATEMENT-3.git
cd VISA-AI-PROBLEM-STATEMENT-3
```

#### Step 2: Backend Setup (The Brain)

1.  **Navigate**: `cd backend`
2.  **Create Environment**:
    - Windows: `python -m venv .venv`
    - Mac/Linux: `python3 -m venv .venv`
3.  **Activate**:
    - Windows: `.venv\Scripts\activate`
    - Mac/Linux: `source .venv/bin/activate`
4.  **Install Tools**: `pip install -r requirements.txt`
5.  **Add Secrets**:
    - Create a file named `.env`.
    - Add this line: `GOOGLE_API_KEY=your_actual_key_here`
6.  **Run**: `uvicorn main:app --reload`
    - You should see: `Uvicorn running on http://127.0.0.1:8000`

#### Step 3: Frontend Setup (The Face)

1.  Open a **new** terminal window.
2.  **Navigate**: `cd frontend`
3.  **Install**: `npm install`
4.  **Run**: `npm run dev`
    - You should see: `Local: http://localhost:5173`

---

## 🎮 User Manual: How to Use

**1. The Dashboard**
Open `http://localhost:5173`. You will see a modern, glass-morphism interface. The center is your "Audit Hub".

**2. Analyzying Data**

- Click the **"Upload Dataset"** box.
- Select a CSV file. (Try one with financial columns like `Amount`, `Date`, `Account_ID`).
- **Tip**: If you don't have one, create a simple CSV in Excel with columns "ID", "Amount", "Date" and put some dummy data.

**3. Interpreting Results**
Once processed (approx 3 seconds), you will see:

- **Health Score**: A big number out of 100. Green is good (>80), Red is bad (<50).
- **Radar Chart**: Shows where you are strong/weak (e.g., High Security but Low Completeness).
- **Issues List**: Click on "Critical" to see exactly what failed.

**4. Consultant Mode (Chat)**

- Look at the panel on the right.
- The AI has already read your audit report.
- Ask it: _"Why is my Validity score so low?"_ or _"Write a memo to the CTO explaining these risks."_

**5. Exporting**

- Click **"Export Audit Report"** at the top right.
- A PDF will download. Scroll to the bottom to see the "Cryptographic Fingerprint".

---

## 👨‍💻 Developer Guide: Extending the System

So you want to add a custom rule? Here is how to add a check for **"Forbidden Countries"**.

**Step 1: Open `backend/core/rules_engine.py`**
Find the `RulesEngine` class. Add this method:

```python
def check_forbidden_countries(self, metadata):
    # Check if 'Country' column has 'North Korea' or 'Iran'
    # Remember: We scan distinct values from metadata, not raw rows!

    forbidden = ['North Korea', 'Iran', 'Syria']

    # We assume 'distinct_values' is part of our metadata profile for categorical columns
    if 'Country' in metadata['columns']:
        details = metadata['columns']['Country'].get('distinct_values', [])
        found_forbidden = [c for c in details if c in forbidden]

        if found_forbidden:
             return {
                 "passed": False,
                 "weight": 10,
                 "details": f"Found sanctioned countries: {found_forbidden}"
             }

    return {"passed": True, "weight": 10, "details": "No sanctioned jurisdictions found."}
```

**Step 2: Register the Rule**
In the same file, find the `run_compliance()` method. Add your new function to the list of checks.

**Step 3: Refresh**
Restart your backend (`Ctrl+C` then `uvicorn...`). Upload your file. The new rule will now impact the "Security" score!

---

## 🔗 API Documentation

Developers can integrate FinAUDIT into other apps.

### `POST /api/analyze`

**Purpose**: Main entry point. Accepts a file, returns a full audit.

- **Input**: `Multipart/Form-Data` file (CSV).
- **Output JSON**:
  ```json
  {
    "filename": "transactions.csv",
    "scores": {
      "overall_score": 75.5,
      "dimension_scores": {
        "security": 100,
        "validity": 45.0
      }
    },
    "analysis": {
      "executive_summary": "The dataset shows strong security protocols...",
      "risk_assessment": "Critical failure in Date formats..."
    },
    "provenance": {
      "fingerprint": "a1b2c3d4..."
    }
  }
  ```

### `POST /api/chat`

**Purpose**: Talk to the AI about the dataset.

- **Input JSON**:
  ```json
  {
    "question": "How do I fix the validity errors?",
    "context": { ...full analysis object... }
  }
  ```
- **Output JSON**:
  ```json
  {
    "response": "To fix the validity errors, ensure all Date columns use ISO8601 format..."
  }
  ```

---

## 📖 Glossary of Terms

- **GDPR (General Data Protection Regulation)**: A strict EU law about user privacy. FinAUDIT helps check if you are collecting too much info.
- **PCI DSS**: Rules for handling Credit Cards. You should never store full card numbers.
- **Metadata**: "Data about data". If you have a spreadsheet, the _rows_ are data. The _fact_ that Column A is named "Age" and has an average of 34 is metadata.
- **PII (Personally Identifiable Information)**: Names, SSNs, Emails. Stuff that identifies a human.
- **LLM (Large Language Model)**: The AI technology behind Gemini/GPT.
- **Provenance**: The history and origin of a document. We use crypto-hashing to prove the document hasn't changed.
- **FastAPI**: The super-fast Python framework we use for the backend.
- **Vite**: A modern tool for building React websites extremely quickly.

---

## ❓ Troubleshooting & FAQ

**Q: The AI chat isn't working/replying!**

- **A**: This almost always means your **Google API Key** is missing or invalid. Check your `.env` file in the `backend` folder. Did you restart the server after adding it?

**Q: I get "Upload Failed: 500 Internal Server Error".**

- **A**: The backend likely crashed while trying to read your CSV.
  1. Check your terminal output for the specific Python error.
  2. Ensure your CSV is comma-separated, not semicolon-separated.
  3. Ensure the file isn't empty.

**Q: Why are all my scores 100?**

- **A**: If your columns are named generically (e.g., `Col1`, `Col2`), our heuristic detector might not know what rules to apply. Renaming columns to `Email`, `Amount`, `Date` helps the system categorize them.

**Q: Can I run this with Docker?**

- **A**: Yes! The project includes a `Dockerfile` (or is Docker-ready). You can build a container to host it on AWS/GCP/Render easily.

---

## 👥 Collaborators

| Name                | Role            | GitHub                                                 |
| :------------------ | :-------------- | :----------------------------------------------------- |
| **Anish Ramesh**    | Developer       | [@Anish-Ramesh](https://github.com/Anish-Ramesh)       |
| **Ganesh Arihanth** | Developer       | [@GaneshArihanth](https://github.com/GaneshArihanth)   |
| **Boopendranath**   | Lead Researcher | [@swankystark](https://github.com/swankystark)         |
| **Eashwar Kumar**   | Lead Tester     | [@Eashwar-Kumar-T](https://github.com/Eashwar-Kumar-T) |

---

**License:** MIT Open Source
**Version:** 2.0 (Agentic Release)
