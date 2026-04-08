
# ⚖️ Legal Case Search Engine + AI Chatbot (DigiVakil)

A full-stack legal case search engine that processes Indian legal PDFs, enables fast full-text search, and now includes an **AI-powered chatbot and case summarizer**.

---

## 🚀 Overview

This project builds a **mini legal search engine + AI assistant** that:

1. Stores legal case PDFs in Azure Blob Storage
2. Extracts text from PDFs using PyMuPDF
3. Stores structured + indexed data in SQLite
4. Uses **FTS5 (Full-Text Search)** for fast keyword queries
5. Provides a **Flask API + frontend UI** for searching cases
6. Allows filtering by **year and court type**
7. Lets users **open PDFs directly from results**
8. Integrates **Gemini AI chatbot (Node.js backend)**
9. Enables **case-specific Q&A and summarization**

---

## 🏗️ Tech Stack

* **Backend (Search API):** Python (Flask)
* **AI Backend:** Node.js (Express + Gemini API)
* **Database:** SQLite (with FTS5)
* **Storage:** Azure Blob Storage
* **PDF Processing:** PyMuPDF (fitz)
* **Frontend:** HTML + CSS + JavaScript
* **Environment Management:** python-dotenv

---

## 📂 Project Structure

```

digivakil/
│
├── app.py                  # Flask app (search API + UI)
├── server.js               # Node.js server (AI chatbot + summarizer)
├── process_pdfs.py         # Basic PDF preview script
├── process_to_sqlite.py    # Full pipeline (Azure → SQLite + FTS)
├── legal.db                # SQLite database (generated)
├── templates/
│   └── index.html          # Frontend UI (search + chatbot)
├── venv/                   # Python virtual environment
├── .env                    # Environment variables
├── .gitignore
└── README.md

```

---

## 🔄 Pipeline Flow

```

Azure Blob Storage (PDFs)
↓
Download PDFs using Azure SDK
↓
Extract text using PyMuPDF
↓
Extract metadata:
- Title (filename)
- Year (regex)
- Court type (keyword detection)
↓
Store in SQLite (structured table)
↓
Index using FTS5 (full-text search)
↓
Flask API (search + filters)
↓
Frontend UI
↓
Node.js AI Backend (Gemini)
↓
Case Q&A + Summarization

```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```

git clone [https://github.com/rohanshenoy30/digivakil.git](https://github.com/rohanshenoy30/digivakil.git)
cd digivakil

```

---

### 2. Activate virtual environment

```

source /Users/rohanshenoy/Desktop/digivakil/venv/bin/activate

```

---

### 3. Install Python dependencies

```

pip install azure-storage-blob pymupdf flask python-dotenv flask-cors

```

---

### 4. Install Node dependencies

```

npm install express cors dotenv @google/generative-ai

```

---

### 5. Setup environment variables

Create a `.env` file:

```

AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
GEMINI_API_KEY=your_gemini_api_key

```

---

### 6. Upload PDFs to Azure

* Create a container: `cases`
* Upload PDFs inside folder: `pdf/`

---

### 7. Process PDFs → SQLite (with FTS)

```

python process_to_sqlite.py

```

This will:

* Extract text from PDFs
* Detect **year and court type**
* Store structured data in SQLite
* Create **FTS5 search index**

---

### 8. Run servers

#### Start Flask (Search API)

```

python app.py

```

#### Start Node.js (AI Chatbot)

```

node server.js

```

---

### 9. Open UI

```

[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

---

## 🔍 Features

### ✅ Search Engine

* Full-text search using SQLite FTS5
* Fast keyword-based retrieval

---

### ✅ Filters

* Filter by **year**
* Filter by **court type**

  * Supreme Court
  * High Court
  * District Court

---

### ✅ UI

* Clean modern frontend
* Interactive search interface
* Scrollable case results

---

### ✅ PDF Access

* Open original case PDFs directly from Azure Blob Storage

---

### 🤖 AI Chatbot (NEW)

* Global chatbot for general legal queries
* Powered by **Google Gemini API**
* Handles natural language questions

---

### ⚖️ Case-Specific AI Q&A (NEW)

* Ask questions about a specific case
* Uses **case content as context**
* Provides:
  * Explanation of case
  * Legal reasoning
  * Key outcomes

---

### 📄 AI Case Summarization (NEW)

* Automatically summarizes judgments
* Supports prompts like:
  * “Summarize this case”
  * “Explain in 5 bullet points”
* Converts long legal text into readable insights

---

### 🧠 Intelligent Context Handling

* Sends case content to AI model
* Enables contextual answers instead of generic responses

---


---

## ⚠️ Limitations (Current Version)

* Gemini API may return **503 errors under high load**
* Large case files may be truncated
* Basic ranking (no BM25 tuning yet)
* Metadata extraction is heuristic-based
* No pagination
* No authentication / access control

---

## 🚀 Future Improvements

* 🔥 Semantic search (embeddings + vector DB)
* 🔍 Hybrid ranking (BM25 + semantic)
* 📄 Better summarization pipelines (chunking + RAG)
* ☁️ Cloud deployment (Azure / Render)
* 🧠 Full RAG-based legal assistant
* 📊 Search analytics dashboard
* 🔐 Secure PDF access using SAS tokens
* ⚡ Streaming responses (ChatGPT-style UI)

---

## 🧠 Key Learning Outcomes

* End-to-end **data pipeline design**
* Working with **Azure Blob Storage**
* PDF parsing and text extraction
* Building **search engines using SQLite FTS**
* Integrating **AI (LLMs) into applications**
* Handling **real-world API issues (rate limits, retries)**
* Full-stack system design (DB + API + AI + UI)

---

## 👨‍💻 Author

**Rohan Shenoy**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
