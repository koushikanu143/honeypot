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

    return """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Access Denied</title>
  <style>
    body{
      margin:0;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      background:
        radial-gradient(circle at top left, rgba(0,255,170,0.08), transparent 30%),
        radial-gradient(circle at bottom right, rgba(0,170,255,0.08), transparent 30%),
        #020406;
      color:#eafff7;
      font-family:Consolas, monospace;
    }
    body::before{
      content:"";
      position:fixed;
      inset:0;
      background-image:
        linear-gradient(rgba(0,255,170,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,170,0.05) 1px, transparent 1px);
      background-size:40px 40px;
      z-index:0;
    }
    .box{
      position:relative;
      z-index:1;
      width:90%;
      max-width:760px;
      background:rgba(5,10,14,0.92);
      border:1px solid rgba(0,255,170,0.18);
      border-radius:24px;
      padding:36px;
      box-shadow:0 0 40px rgba(0,255,170,0.08);
    }
    .badge{
      display:inline-block;
      margin-bottom:16px;
      padding:8px 14px;
      border-radius:999px;
      background:rgba(0,255,170,0.08);
      border:1px solid rgba(0,255,170,0.18);
      color:#8effd8;
      font-size:12px;
    }
    h1{
      margin:0 0 12px 0;
      color:#ff6464;
      font-size:44px;
    }
    h2{
      margin:0 0 16px 0;
      color:#61ffd0;
      font-size:22px;
    }
    p{
      color:#b8e8dc;
      line-height:1.8;
      font-size:15px;
    }
    .terminal{
      margin-top:22px;
      padding:18px;
      border-radius:18px;
      border:1px solid rgba(0,255,170,0.16);
      background:#010303;
    }
    .terminal div{
      color:#35ffb4;
      margin-bottom:10px;
      font-size:14px;
    }
    .terminal div:last-child{
      margin-bottom:0;
    }
    .btn{
      display:inline-block;
      margin-top:24px;
      text-decoration:none;
      color:#02140d;
      background:linear-gradient(90deg,#2effb8,#36d9ff);
      padding:14px 20px;
      border-radius:16px;
      font-weight:bold;
    }
  </style>
</head>
<body>
  <div class='box'>
    <div class='badge'>Authentication Monitoring Event</div>
    <h1>ACCESS DENIED</h1>
    <h2>Unauthorized Session Rejected</h2>
    <p>
      The requested authentication session could not be validated by the monitored security gateway.
      This honeypot environment records suspicious access patterns for cyber security demonstration and analysis.
    </p>
    <div class='terminal'>
      <div>> Session verification: FAILED</div>
      <div>> Threat log updated successfully</div>
      <div>> Source activity flagged for monitoring</div>
      <div>> Security dashboard notification generated</div>
    </div>
    <a class='btn' href='/'>Return to Secure Gateway</a>
  </div>
</body>
</html>
"""

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