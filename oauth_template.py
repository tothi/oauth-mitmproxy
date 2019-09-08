import requests

REFRESH_TOKEN = open("refresh_token.txt", "r").read().strip()
CLIENT_ID = "client_id"
AUTH_URI = "https://example.com/api/authentication/"

def refresh_token(refresh_token):
    # in case of bad SSL certs, add: verify=False
    r = requests.post(AUTH_URI, data={"grant_type": "refresh_token", "refresh_token": refresh_token, "client_id": CLIENT_ID})
    assert r.status_code == 200
    assert r.json()['token_type'] == 'Bearer'
    open("refresh_token.txt", "w").write(r.json()['refresh_token'])
    return (r.json()['refresh_token'], r.json()['access_token'])
