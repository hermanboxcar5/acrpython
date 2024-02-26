import os
import requests
import time
import json
import threading

from flask import Flask

app = Flask(__name__)

# Credentials
username = os.environ.get('username')
password = os.environ.get('password')

last_request_timestamp = None

def claim_timed_bonus():
    global last_request_timestamp
    while True:
        response = authenticate_user()
        token = json.loads(response.content)['token']
        response = collect_timed_bonus(token)
        last_request_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1801)  # Sleep for approximately 30 minutes

def authenticate_user():
    response = requests.post(
        "https://dev-nakama.winterpixel.io/v2/account/authenticate/email?create=false",
        data=json.dumps({
            "email": username,
            "password": password,
            "vars": {
                "client_version": "99999"
            }
        }),
        headers={
            "authorization":
            "Basic OTAyaXViZGFmOWgyZTlocXBldzBmYjlhZWIzOTo="
        })
    return response

def collect_timed_bonus(token):
    payload = '"{}"'
    response = requests.post(
        "https://dev-nakama.winterpixel.io/v2/rpc/collect_timed_bonus",
        headers={"authorization": f"Bearer {token}"},
        data=payload.encode('utf-8'))
    return response

@app.route('/')
def last_request_time():
    global last_request_timestamp
    if last_request_timestamp:
        return f"Last request sent at: {last_request_timestamp}"
    else:
        return "No requests sent yet."

if __name__ == "__main__":
    # Start a background thread to claim timed bonus
    claim_timed_bonus_thread = threading.Thread(target=claim_timed_bonus)
    claim_timed_bonus_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
