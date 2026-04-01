# ⚖️ Legal Case Search Engine (Azure + SQLite)

A simple search engine for Indian legal case documents using Azure Blob Storage, PDF parsing, and SQLite.

---

## 🚀 Overview

This project builds a mini legal search system that:

1. Stores legal case PDFs in Azure Blob Storage  
2. Extracts text from PDFs using PyMuPDF  
3. Stores structured data in SQLite  
4. Allows keyword-based search using a Flask API  

---

## 🏗️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Storage:** Azure Blob Storage
- **PDF Processing:** PyMuPDF (fitz)
- **Environment Management:** python-dotenv

---

## 📂 Project Structure

```
digivakil/
│
├── app.py                  # Flask API (search endpoint)
├── process_pdfs.py         # Reads PDFs from Azure (basic preview)
├── process_to_sqlite.py    # Extracts + stores data in SQLite
├── legal.db                # SQLite database (generated)
├── templates/
│   └── index.html          # Basic frontend UI
├── .env                    # Environment variables (not pushed)
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
Clean + parse metadata (title, year)
↓
Store in SQLite database
↓
Flask API
↓
Search results (JSON / UI)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rohanshenoy30/digivakil.git
cd digivakil
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install azure-storage-blob pymupdf flask python-dotenv
```

---

### 4. Setup environment variables

Create a `.env` file:

```env
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
```

---

### 5. Upload PDFs to Azure

- Create a container called: `cases`  
- Upload PDFs inside a folder: `pdf/`  

---

### 6. Process PDFs → SQLite

```bash
python process_to_sqlite.py
```

This will:
- Extract text from PDFs  
- Store data in `legal.db`  

---

### 7. Run Flask server

```bash
python app.py
```

---

### 8. Search

Open browser:

```
http://127.0.0.1:5000/search?q=murder
```

---

## 🔍 Example Output

```json
[
  {
    "title": "STATE OF MAHARASHTRA vs XYZ",
    "year": 1970,
    "preview": "Supreme Court of India..."
  }
]
```

---

## 📌 Features

- Keyword-based legal case search  
- Azure cloud storage integration  
- Local database for fast querying  
- PDF text extraction pipeline  

---

## ⚠️ Limitations (Current Version)

- Basic keyword search (no ranking)  
- No pagination  
- Limited metadata extraction  
- No authentication  

---

## 🚀 Future Improvements

- 🔥 Full-text search (FTS5 in SQLite)  
- 🔍 Better ranking (BM25 / embeddings)  
- 🌐 UI improvements  
- 📄 Open PDF directly from results  
- ☁️ Move to Cosmos DB / Elasticsearch  

---

## 👨‍💻 Author

**Rohan Shenoy**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
