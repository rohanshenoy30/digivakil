from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# 🔑 Replace with your storage account name
STORAGE_ACCOUNT = "legalstoragerohanproject"
CONTAINER_NAME = "cases"


def get_db():
    conn = sqlite3.connect("legal.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    q = request.args.get("q", "")
    year = request.args.get("year", "")
    court = request.args.get("court", "")

    conn = get_db()
    cursor = conn.cursor()

    # Base SQL
    sql = """
    SELECT cases.id, cases.title, cases.year, cases.court,
           substr(cases.content, 1, 300) as preview
    FROM cases_fts
    JOIN cases ON cases.id = cases_fts.id
    WHERE cases_fts MATCH ?
    """

    params = [q if q else "*"]

    # Filters
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
                "title": row["title"],
                "year": row["year"],
                "court": row["court"],
                "preview": row["preview"],
                "pdf_url": pdf_url
            })

    except Exception as e:
        return jsonify({"error": str(e)})

    conn.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)