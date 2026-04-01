from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
# 🔑 CONFIG
BLOB_CONNECTION = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

CONTAINER_NAME = "cases"

# 🔌 Connect to Blob
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION)
container = blob_service.get_container_client(CONTAINER_NAME)

# 🗄️ Create SQLite DB
conn = sqlite3.connect("legal.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cases (
    id TEXT PRIMARY KEY,
    title TEXT,
    year INTEGER,
    content TEXT
)
""")

# 🚀 Process PDFs
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

        filename = blob.name.split("/")[-1]

        # Simple year extraction
        year = 1950
        for y in range(1950, 2025):
            if str(y) in text:
                year = y
                break

        # Insert into SQLite
        cursor.execute("""
        INSERT OR REPLACE INTO cases (id, title, year, content)
        VALUES (?, ?, ?, ?)
        """, (
            blob.name,
            filename,
            year,
            text[:50000]  # larger limit since local DB
        ))

        conn.commit()

        print(f"✅ Inserted: {filename}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

conn.close()

print("\n🎉 DONE: Data stored in SQLite!")