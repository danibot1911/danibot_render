import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

# Variables de entorno desde Render
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

# Cliente de Slack
client = WebClient(token=SLACK_BOT_TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "¡DaniBot está activo en Render!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Verificación inicial de Slack (challenge)
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Evento normal de mensaje
    if data.get("type") == "event_callback":
        event = data.get("event", {})

        if event.get("type") == "message" and "subtype" not in event:
            user = event.get("user")
            text = event.get("text")
            channel = event.get("channel")

            if user and text:
                try:
                    client.chat_postMessage(
                        channel=channel,
                        text=f"Hola <@{user}>! Recibido: {text}"
                    )
                except SlackApiError as e:
                    print(f"Error enviando mensaje: {e.response['error']}")

        return "OK", 200  # <<<< ESTE return debe estar aquí dentro

# Lanzar en el puerto asignado por Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
