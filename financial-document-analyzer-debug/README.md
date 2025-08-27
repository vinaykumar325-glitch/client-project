Financial Document Analyzer – Debug Assignment
Project Overview

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.
It supports PDF uploads, extracts financial metrics, assesses risks, and provides market insights.

Getting Started
1. Install Required Libraries
pip install -r requirements.txt

2. Run the API
uvicorn main:app --reload

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

## Overview
This project is a fixed, robust version of the Financial Document Analyzer originally built with CrewAI. It addresses deterministic bugs, removes unsafe assumptions, and improves prompt clarity.

### What I fixed
- **Module import resilience**: code no longer crashes if `crewai`/`crewai_tools` are absent.
- **`TypeError: 'NoneType' object is not subscriptable`**: fixed by safe handling of `document_text` (never sliced when `None`).
- **Unsafe prompts**: replaced "make up" instructions with structured, factual prompts. Agents now extract and summarize actual content.
- **File handling & PDF reading**: Added robust PDF/text loaders with helpful fallbacks.


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


All deterministic bugs fixed.

Prompts rewritten for efficiency.

Bonus scaffolding included (Celery + DB).
