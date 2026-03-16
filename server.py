from flask import Flask, request, render_template, jsonify
import datetime
import json
import os

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Firebase from environment variables
service_account = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
}

cred = credentials.Certificate(service_account)
firebase_admin.initialize_app(cred)
db = firestore.client()

LOG_FILE = "honeypot_logs.json"

def save_log(data):
    # Save to Firestore
    db.collection('honeypot_logs').add(data)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/trap",methods=["POST"])
def trap():

    username = request.form.get("username")
    password = request.form.get("password")

    ip = request.remote_addr

    browser = request.headers.get("User-Agent")

    time = str(datetime.datetime.now())

    data = {
        "time":time,
        "ip":ip,
        "username":username,
        "password":password,
        "browser":browser
    }

    save_log(data)

    return "Login Failed"

@app.route("/logs")
def logs():
    # Fetch from Firestore
    logs_ref = db.collection('honeypot_logs')
    docs = logs_ref.stream()
    logs = []
    for doc in docs:
        log_data = doc.to_dict()
        log_data['id'] = doc.id  # Include document ID if needed
        logs.append(log_data)
    return jsonify(logs)

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000)