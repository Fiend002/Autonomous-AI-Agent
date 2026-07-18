# 🤖 Autonomous AI Agent

A simple, beginner-friendly autonomous AI agent built with **FastAPI**, the
**Groq API**, and **python-docx** — with a **Streamlit** web frontend.

You give it a plain-English request. It plans the work by itself, writes each
section, and hands you a professional Microsoft Word document.

No LangChain. No CrewAI. No AutoGen. No LangGraph. Just clear Python you can
read, understand, and explain line by line.

---

## Project Overview

The agent takes a natural-language request such as *"Create a business proposal
for an AI Resume Screening System"* and:

1. Uses the LLM to **generate its own TODO list** of sections (not hardcoded).
2. Loops through the list and **writes each section** one at a time.
3. **Combines** everything into a single professional `.docx` document.
4. **Saves** it to the `output/` folder and returns a JSON summary.

A Streamlit page sits in front of the API so you can use it from a browser
without touching a terminal after startup.

---

## Architecture

```
        ┌──────────────┐        HTTP POST         ┌──────────────────┐
        │  Streamlit   │  ───────────────────────▶ │   FastAPI        │
        │  (app.py)    │   {"request": "..."}      │   (main.py)      │
        │  the FACE    │  ◀─────────────────────── │   the BRAIN STEM │
        └──────────────┘        JSON result        └────────┬─────────┘
                                                            │
                     ┌──────────────────────────────────────┼───────────────────┐
                     ▼                     ▼                 ▼                    ▼
              ┌────────────┐        ┌────────────┐   ┌───────────────┐   ┌──────────────┐
              │ planner.py │        │ executor.py│   │doc_generator  │   │   llm.py     │
              │ makes the  │        │ writes each│   │ builds .docx  │   │ Groq API     │
              │ TODO list  │        │ section    │   │ file          │   │ (used by both│
              └─────┬──────┘        └─────┬──────┘   └───────────────┘   │  planner &   │
                    │                     │                              │  executor)   │
                    └────────► llm.py ◄───┘                              └──────────────┘
```

The design principle is **one file, one job**. That makes the project easy to
explain and easy to modify.

---

## Folder Structure

```
autonomous-ai-agent/
│── main.py            # FastAPI server + POST /agent endpoint
│── app.py             # Streamlit frontend (calls the API)
│── llm.py             # Groq API integration (ask_llm)
│── planner.py         # Generates the TODO list autonomously
│── executor.py        # Writes content for each task/section
│── doc_generator.py   # Builds the .docx file with python-docx
│── requirements.txt   # All dependencies
│── .env.example       # Example API key config
│── README.md          # This file
│── output/            # Generated Word documents land here
```

---

## Installation

1. **Clone / unzip** the project and enter the folder:

   ```bash
   cd autonomous-ai-agent
   ```

2. **(Recommended) create a virtual environment:**

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Groq API key.** Get a free key at
   <https://console.groq.com/keys>, then:

   ```bash
   # copy the example file
   cp .env.example .env        # Windows: copy .env.example .env
   ```

   Open `.env` and paste your key:

   ```
   GROQ_API_KEY=gsk_your_real_key_here
   ```

---

## How to Run

You need **two terminals** — one for the backend, one for the frontend.

**Terminal 1 — start the FastAPI backend:**

```bash
uvicorn main:app --reload
```

The API is now at <http://127.0.0.1:8000>.
Interactive docs: <http://127.0.0.1:8000/docs>.

**Terminal 2 — start the Streamlit frontend:**

```bash
streamlit run app.py
```

Your browser opens automatically. Type a request, click **Run Agent**, and
download the finished document.

> You can also use the API on its own without Streamlit — see below.

---

## API Usage

### Endpoint

```
POST /agent
```

### Sample Request

```json
{
  "request": "Create a business proposal for an AI Resume Screening System."
}
```

You can test it directly with curl:

```bash
curl -X POST http://127.0.0.1:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"request": "Create a business proposal for an AI Resume Screening System."}'
```

### Sample Response

```json
{
  "status": "success",
  "original_request": "Create a business proposal for an AI Resume Screening System.",
  "generated_plan": [
    "Executive Summary",
    "Problem Statement",
    "Proposed Solution",
    "Key Features",
    "Timeline",
    "Budget",
    "Conclusion"
  ],
  "output_file_path": "output/document_20260708_120500.docx",
  "message": "Document generated successfully."
}
```

---

## Engineering Improvement: Multi-Step Planning

The required engineering improvement is **Multi-Step Planning**.

Instead of asking the LLM to write an entire document in one giant prompt, the
agent works in two phases:

```
User Request
     ↓
LLM generates a TODO list          ← planner.py  (autonomous, not hardcoded)
     ↓
Python executes each task in turn  ← executor.py (one focused LLM call per section)
     ↓
Combine all sections
     ↓
Generate DOCX                      ← doc_generator.py
     ↓
Return JSON response               ← main.py
```

**Why this is better:**

- **Focus:** Each LLM call handles one small section, so answers are more
  detailed and accurate than a single "write everything" prompt.
- **Autonomy:** The plan is created by the LLM at runtime based on the request,
  so the agent adapts to *any* task — proposals, project plans, reports, etc.
- **Robustness:** If one section fails, the others still succeed (the executor
  catches per-section errors).
- **Explainability:** You can see the plan the agent made, which is exactly what
  makes it feel "autonomous" rather than a fixed template.

---

## Test Cases

### Test Case 1 — Business Proposal

```json
{ "request": "Create a business proposal for an AI Resume Screening System." }
```

### Test Case 2 — Project Plan with Missing Info

```json
{
  "request": "Create a project plan for an Inventory Management System. Budget is not provided, so choose a reasonable timeline and clearly state any assumptions."
}
```

For Test Case 2 the agent **detects the missing budget/timeline** and, inside
the relevant sections, makes reasonable assumptions and states them explicitly
(this behaviour is instructed in `executor.py`).

---

## Future Improvements

- **Persistence:** Save each run's plan and output to a small database.
- **Streaming:** Show sections in the UI as they are written, live.
- **Templates & branding:** Add cover pages, logos, and house styles to the DOCX.
- **Retries:** Automatically retry a failed section before giving up.
- **PDF export:** Offer a PDF version alongside the Word file.
- **Model choice:** Let the user pick the Groq model from the Streamlit sidebar.
- **Tool use:** Let sections call real tools (web search, calculators) not just text.
```
