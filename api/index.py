import os
import requests
import time
import json

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

def handler(request):
    global last_request_timestamp
    if request.method == 'GET':
        if last_request_timestamp:
            return {
                'statusCode': 200,
                'body': f'Last request sent at: {last_request_timestamp}'
            }
        else:
            return {
                'statusCode': 200,
                'body': 'No requests sent yet.'
            }
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }
