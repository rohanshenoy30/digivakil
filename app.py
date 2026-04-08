from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv
from google import genai

# ---------------- LOAD ENV ----------------
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow frontend requests

# ---------------- GEMINI SETUP ----------------
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Azure storage config
STORAGE_ACCOUNT = "legalstoragerohanproject"
CONTAINER_NAME = "cases"


# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("legal.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SEARCH ----------------
@app.route("/search")
def search():
    q = request.args.get("q", "")
    year = request.args.get("year", "")
    court = request.args.get("court", "")

    conn = get_db()
    cursor = conn.cursor()

    sql = """
    SELECT cases.id, cases.title, cases.year, cases.court,
           substr(cases.content, 1, 300) as preview
    FROM cases_fts
    JOIN cases ON cases.id = cases_fts.id
    WHERE cases_fts MATCH ?
    """

    params = [q if q else "*"]

    if year:
        sql += " AND cases.year = ?"
        params.append(year)

    if court:
        sql += " AND cases.court = ?"
        params.append(court)

    sql += " LIMIT 20"

    results = []

    try:
        for row in cursor.execute(sql, params):
            pdf_url = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/{CONTAINER_NAME}/{row['id']}"

            results.append({
                "id": row["id"],
                "title": row["title"],
                "year": row["year"],
                "court": row["court"],
                "preview": row["preview"],
                "pdf_url": pdf_url
            })

    except Exception as e:
        print("❌ SEARCH ERROR:", e)

    conn.close()
    return jsonify(results)


# ---------------- GEMINI FUNCTION ----------------
def ask_gemini(question, context):
    print("🧠 Sending request to Gemini...")

    try:
        prompt = f"""
You are a legal assistant.

Context:
{context[:3000]}

Question:
{question}

Answer clearly in simple terms:
"""

        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        print("✅ Gemini responded")

        return response.text if response.text else "No response generated."

    except Exception as e:
        print("❌ GEMINI ERROR:", e)
        return "⚠️ Error generating answer from AI."


# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    print("🔥 CHAT ENDPOINT HIT")

    try:
        data = request.json
        print("📩 DATA RECEIVED:", data)

        question = data.get("question")
        case_id = data.get("case_id")

        if not question or not case_id:
            return jsonify({"error": "Missing question or case_id"})

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT content FROM cases WHERE id = ?", (case_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({"error": "Case not found"})

        print("📄 Case content fetched")

        answer = ask_gemini(question, row["content"])

        return jsonify({"answer": answer})

    except Exception as e:
        print("❌ CHAT ERROR:", e)
        return jsonify({"error": str(e)})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)