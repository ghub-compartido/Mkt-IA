from flask import Flask, redirect, request, jsonify
import requests
import secrets

app = Flask(__name__)

CLIENT_KEY = "sbawvvv4vg75pasjib"
CLIENT_SECRET = "Dpn1oi36AD78RlPVxQ8NVeBVkQ5D2vuk"
REDIRECT_URI = "https://cea86225fa63.ngrok-free.app/auth/tiktok/callback"

state_store = {}

@app.route("/")
def index():
    return '<a href="/login">Conectar con TikTok</a>'

@app.route("/login")
def login():
    state = secrets.token_urlsafe(16)
    state_store[state] = True

    auth_url = (
        "https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={CLIENT_KEY}"
        f"&response_type=code"
        f"&scope=video.publish"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
    )

    return redirect(auth_url)

@app.route("/auth/tiktok/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or state not in state_store:
        return "Error de autenticación", 400

    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    r = requests.post(token_url, data=data)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
