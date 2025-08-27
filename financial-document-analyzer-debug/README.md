Financial Document Analyzer – Debug Assignment
Project Overview

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.
It supports PDF uploads, extracts financial metrics, assesses risks, and provides market insights.

Getting Started
1. Install Required Libraries
pip install -r requirements.txt

2. Run the API
uvicorn main:app --reload


Open http://127.0.0.1:8000/docs
 to interact with the API.

Sample Document

The system analyzes financial documents like Tesla’s Q2 2025 financial update.

Download from: Tesla Q2 2025 Update PDF

Save it as:

data/sample.pdf


Or upload any PDF through the API endpoint.

⚠️ Note: data/sample.pdf is currently a placeholder — replace it with the actual Tesla report for testing.

Debugging Instructions

🐛 Debug Mode Activated! — This project initially contained multiple bugs.

Your mission was to:

Identify the Bug: Each file had at least one error.

Fix the Bug: Implement corrections.

Test the Fix: Run the project and confirm functionality.

Repeat: Continue until stable.

Expected Features

✅ Upload financial documents (PDF/TXT)

✅ AI-powered financial analysis

✅ Investment recommendations

✅ Risk assessment

✅ Market insights

Bugs Found & Fixes
1. Module Import Errors

Bug: ModuleNotFoundError: crewai

Fix: Added local fallback LocalLLM and safe imports.

2. NoneType Subscript Bug

Bug: TypeError: 'NoneType' object is not subscriptable when slicing document_text.

Fix: Added safe handling for None and non-string inputs.

3. Wrong Parameter Name

Bug: Used tool= instead of tools= when creating Agents.

Fix: Corrected to tools=.

4. File Handling Issues

Bug: PDF/Text reading failures crashed tasks.

Fix: Added robust PDFLoader with fallbacks.

5. Inefficient Prompts

Bug: Prompts instructed AI to "make up" or were vague.

Fix: Rewritten as clear, factual, structured prompts (metrics, risks, insights).

Setup & Usage
Run Local Tests
python main.py


This runs a built-in harness that:

Reads a sample financial text file

Tests with no file input

Tests with None, empty, and invalid document text

API Documentation
Endpoints
GET /

Health check

POST /analyze

Inputs:

file: Financial PDF or TXT

query: Analysis request (string)

Response:

{
  "status": "success",
  "query": "Summarize Tesla's revenue",
  "analysis": {
    "task_0_Financial Document Verifier": {...},
    "task_1_Senior Financial Analyst": {...}
  }
}

Bonus Features (Optional)

Queue Worker Model:

Implemented celery_worker.py with Redis backend for concurrent request handling.

Run with:

celery -A celery_worker worker --loglevel=info


Database Integration:

Implemented db.py using SQLite to store queries & results.

Functions: init_db(), save_analysis(query, result)

Final Notes

Tested against TSLA-Q2-2025-Update.pdf.

All deterministic bugs fixed.

Prompts rewritten for efficiency.

Bonus scaffolding included (Celery + DB).
