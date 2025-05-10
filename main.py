import os
import slack_sdk
from flask import Flask

app = Flask(__name__)

slack_token = os.environ.get("SLACK_BOT_TOKEN")
channel_id = os.environ.get("SLACK_CHANNEL_ID")
client = slack_sdk.WebClient(token=slack_token)

@app.route("/")
def send_message():
    try:
        client.chat_postMessage(channel=channel_id, text="¡DaniBot está activo en Render!")
        return "Mensaje enviado a Slack correctamente."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
