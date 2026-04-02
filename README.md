# ⚖️ Legal Case Search Engine (Azure + SQLite + FTS)

A full-stack legal case search engine that processes Indian legal PDFs, stores them efficiently, and provides fast full-text search with filters and a modern UI.

---

## 🚀 Overview

This project builds a **mini legal search engine** that:

1. Stores legal case PDFs in Azure Blob Storage
2. Extracts text from PDFs using PyMuPDF
3. Stores structured + indexed data in SQLite
4. Uses **FTS5 (Full-Text Search)** for fast keyword queries
5. Provides a **Flask API + frontend UI** for searching cases
6. Allows filtering by **year and court type**
7. Lets users **open PDFs directly from results**

---

## 🏗️ Tech Stack

* **Backend:** Python (Flask)
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
├── app.py                  # Flask app (API + UI routing)
├── process_pdfs.py         # Basic PDF preview script
├── process_to_sqlite.py    # Full pipeline (Azure → SQLite + FTS)
├── legal.db                # SQLite database (generated)
├── templates/
│   └── index.html          # Styled frontend UI
├── .env                    # Environment variables (NOT pushed)
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
Flask API
↓
Frontend UI (search + filters + PDF open)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/rohanshenoy30/digivakil.git
cd digivakil
```

---

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```
pip install azure-storage-blob pymupdf flask python-dotenv
```

---

### 4. Setup environment variables

Create a `.env` file:

```
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
```

---

### 5. Upload PDFs to Azure

* Create a container: `cases`
* Upload PDFs inside folder: `pdf/`

---

### 6. Process PDFs → SQLite (with FTS)

```
python process_to_sqlite.py
```

This will:

* Extract text from PDFs
* Detect **year and court type**
* Store structured data in SQLite
* Create **FTS5 search index**

---

### 7. Run Flask server

```
python app.py
```

---

### 8. Open UI

```
http://127.0.0.1:5000
```

---

## 🔍 Features

### ✅ Search

* Full-text search using SQLite FTS5
* Fast and efficient keyword matching

### ✅ Filters

* Filter by **year**
* Filter by **court type**

  * Supreme Court
  * High Court
  * District Court

### ✅ UI

* Clean modern frontend
* Styled search interface
* Scrollable results

### ✅ PDF Access

* Open original case PDF directly from Azure Blob

### ✅ Metadata Extraction

* Title (from filename)
* Year (regex-based)
* Court (keyword-based detection)

---

## 🔍 Example API Output

```
[
  {
    "title": "STATE_OF_MAHARASHTRA.pdf",
    "year": 1970,
    "court": "Supreme Court",
    "preview": "SUPREME COURT OF INDIA...",
    "pdf_url": "https://<storage>.blob.core.windows.net/cases/pdf/file.pdf"
  }
]
```

---

## ⚠️ Limitations (Current Version)

* Basic ranking (no BM25 tuning yet)
* Metadata extraction is heuristic-based
* No pagination (limited to top results)
* No authentication / access control
* Azure Blob uses public access (for PDF viewing)

---

## 🚀 Future Improvements

* 🔥 Semantic search (OpenAI / embeddings)
* 🔍 Better ranking (BM25 / hybrid search)
* 📄 Case summarization using LLMs
* ☁️ Deploy to cloud (Render / Azure App Service)
* 🧠 Convert to RAG-based legal assistant
* 📊 Add analytics (most searched cases)
* 🔐 Secure PDF access using SAS tokens

---

## 🧠 Key Learning Outcomes

* End-to-end **data pipeline design**
* Working with **Azure Blob Storage**
* PDF parsing and text extraction
* Building **search engines using SQLite FTS**
* Backend API design with Flask
* Full-stack integration (UI + API + DB)

---

## 👨‍💻 Author

**Rohan Shenoy**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
