import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_ID = os.environ.get("BOT_ID", "")
POST_URL = "https://api.groupme.com/v3/bots/post"

def send(text):
    if BOT_ID:
        requests.post(POST_URL, json={"bot_id": BOT_ID, "text": text})

@app.route("/", methods=["POST"])
def inbound():
    data = request.get_json(silent=True) or {}
    if data.get("sender_type") == "bot":
        return jsonify(ok=True)

    text = (data.get("text") or "").strip().lower()

    # Command: !mullet or !mulletman
    if text in ("!mullet", "!mulletman"):
        send("🧔‍♂️ Mullet Man: https://en.wikipedia.org/wiki/Matt_Mullins")
    elif text == "!help":
        send("Commands: !mullet, !mulletman, !help")

    return jsonify(ok=True)

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
