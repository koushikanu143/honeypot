from flask import Flask, request, render_template, jsonify
import datetime
import json

app = Flask(__name__)

LOG_FILE = "honeypot_logs.json"

def save_log(data):

    try:
        with open(LOG_FILE) as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(data)

    with open(LOG_FILE,"w") as f:
        json.dump(logs,f,indent=4)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/trap",methods=["POST"])
def trap():

    username = request.form.get("username")

    ip = request.remote_addr

    browser = request.headers.get("User-Agent")

    time = str(datetime.datetime.now())

    data = {
        "time":time,
        "ip":ip,
        "username":username,
        "browser":browser
    }

    save_log(data)

    return "Login Failed"

@app.route("/logs")
def logs():

    try:
        with open(LOG_FILE) as f:
            logs=json.load(f)
    except:
        logs=[]

    return jsonify(logs)

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000)