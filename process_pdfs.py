from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in .env")

container_name = "cases"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

for blob in container_client.list_blobs(name_starts_with="pdf/"):
    if not blob.name.endswith(".pdf"):
        continue

    print(f"\nProcessing: {blob.name}")

    try:
        blob_client = container_client.get_blob_client(blob)
        pdf_bytes = blob_client.download_blob().readall()

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        doc.close()

        print("Preview:", text[:300])

    except Exception as e:
        print(f"Error processing {blob.name}: {e}")