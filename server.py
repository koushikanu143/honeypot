from flask import Flask, request, render_template, jsonify
import datetime
import json
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccount.json")
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