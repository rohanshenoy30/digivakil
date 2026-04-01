from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def search_cases(query):
    conn = sqlite3.connect("legal.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, year, content
    FROM cases
    WHERE content LIKE ?
    LIMIT 10
    """, ('%' + query + '%',))

    results = cursor.fetchall()
    conn.close()

    output = []
    for row in results:
        output.append({
            "title": row[0],
            "year": row[1],
            "preview": row[2][:300]
        })

    return output


@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        results = search_cases(query)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)