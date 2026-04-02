from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF
import sqlite3
from dotenv import load_dotenv
import os
import re

# Load env
load_dotenv()

BLOB_CONNECTION = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "cases"

if not BLOB_CONNECTION:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found")

# Connect to Azure Blob
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION)
container = blob_service.get_container_client(CONTAINER_NAME)

# Create SQLite DB
conn = sqlite3.connect("legal.db")
cursor = conn.cursor()

# Create main table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cases (
    id TEXT PRIMARY KEY,
    title TEXT,
    year INTEGER,
    court TEXT,
    content TEXT
)
""")

# Create FTS table
cursor.execute("""
CREATE VIRTUAL TABLE IF NOT EXISTS cases_fts USING fts5(
    id,
    content
)
""")

# Helper: extract year
def extract_year(text):
    match = re.search(r"(19\d{2}|20\d{2})", text)
    if match:
        return int(match.group(0))
    return 1950

# Helper: extract court
def extract_court(text):
    text = text.upper()
    if "SUPREME COURT" in text:
        return "Supreme Court"
    elif "HIGH COURT" in text:
        return "High Court"
    elif "DISTRICT COURT" in text:
        return "District Court"
    return "Unknown"

# Process PDFs
for blob in container.list_blobs(name_starts_with="pdf/"):

    if not blob.name.endswith(".pdf"):
        continue

    print(f"\nProcessing: {blob.name}")

    try:
        blob_client = container.get_blob_client(blob)
        pdf_bytes = blob_client.download_blob().readall()

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        doc.close()

        filename = blob.name.split("/")[-1]

        year = extract_year(text)
        court = extract_court(text)

        # Insert main table
        cursor.execute("""
        INSERT OR REPLACE INTO cases (id, title, year, court, content)
        VALUES (?, ?, ?, ?, ?)
        """, (
            blob.name,
            filename,
            year,
            court,
            text[:50000]
        ))

        # Insert FTS
        cursor.execute("""
        INSERT OR REPLACE INTO cases_fts (id, content)
        VALUES (?, ?)
        """, (
            blob.name,
            text
        ))

        conn.commit()

        print(f"✅ Inserted: {filename} | {court} | {year}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

conn.close()

print("\n🎉 DONE: Data stored in SQLite with FTS!")