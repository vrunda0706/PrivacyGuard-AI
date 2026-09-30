from flask import Flask, render_template, request, jsonify
import sqlite3, re, os
from datetime import datetime
from ml_model import predict_risk, privacy_score
from recommendations import generate_recommendations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "privacyguard.db")

app = Flask(__name__)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        phone TEXT,
        score INTEGER,
        risk TEXT,
        email_findings INTEGER,
        phone_findings INTEGER,
        breach_findings INTEGER,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()

def demo_findings(email, phone):
    # Portfolio-safe demo provider. No real breach data is queried.
    email_clean = (email or "").strip().lower()
    phone_digits = re.sub(r"\D", "", phone or "")
    email_findings = 0 if not email_clean else (2 if "demo" in email_clean or "example" in email_clean else 1)
    phone_findings = 0 if not phone_digits else (1 if phone_digits.endswith("00000") else 2)
    breach_findings = min(4, email_findings + phone_findings)
    return email_findings, phone_findings, breach_findings

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()

    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Please enter a valid email address."}), 400
    if len(phone) > 30:
        return jsonify({"error": "Phone input is too long."}), 400
    if not email and not phone:
        return jsonify({"error": "Enter an email or phone number for the demo scan."}), 400

    ef, pf, bf = demo_findings(email, phone)
    score = privacy_score(ef, pf, bf)
    risk = "LOW" if score >= 80 else "MEDIUM" if score >= 60 else "HIGH"
    ai = predict_risk(ef, pf, bf)
    recs = generate_recommendations(ef, pf, bf, ai["risk"])

    conn = db()
    conn.execute(
        "INSERT INTO scans(email,phone,score,risk,email_findings,phone_findings,breach_findings,created_at) VALUES(?,?,?,?,?,?,?,?)",
        (email, phone, score, risk, ef, pf, bf, datetime.utcnow().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

    return jsonify({
        "score": score, "risk": risk,
        "email_findings": ef, "phone_findings": pf, "breach_findings": bf,
        "ml": ai, "recommendations": recs,
        "disclaimer": "Demo findings are simulated; no real breach database was queried."
    })

@app.route("/api/history")
def history():
    conn = db()
    rows = conn.execute("SELECT id,score,risk,email_findings,phone_findings,breach_findings,created_at FROM scans ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/permissions", methods=["POST"])
def permissions():
    data = request.get_json(silent=True) or {}
    permissions = data.get("permissions", [])
    risk_map = {"location": 2, "contacts": 2, "camera": 1, "microphone": 1, "storage": 1, "notifications": 0}
    points = sum(risk_map.get(str(p).lower(), 0) for p in permissions)
    level = "HIGH" if points >= 5 else "MEDIUM" if points >= 3 else "LOW"
    return jsonify({"risk": level, "points": points, "message": "Review permissions you do not need."})

init_db()

if __name__ == "__main__":
    app.run(debug=True)
