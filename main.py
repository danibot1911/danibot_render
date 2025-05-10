import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

client = WebClient(token=SLACK_BOT_TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "¡DaniBot está activo en Render!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    if data.get("type") == "event_callback":
        event = data.get("event", {})
        user = event.get("user")
        text = event.get("text")
        channel = event.get("channel")

        if event.get("type") == "message" and user and text:
            try:
                client.chat_postMessage(channel=channel, text=f"Hola <@{user}>! Recibí tu mensaje: {text}")
            except SlackApiError as e:
                print(f"Error enviando mensaje: {e.response['error']}")

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)o
        
