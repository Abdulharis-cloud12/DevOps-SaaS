from flask import Flask, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


@app.route("/", methods=["POST"])
def receive_alert():
    data = request.get_json()

    if not data or "alerts" not in data:
        return {"error": "Invalid Alertmanager payload"}, 400

    messages = []

    for alert in data["alerts"]:
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        status = alert.get("status", "unknown")
        alert_name = labels.get("alertname", "Unknown alert")
        pipeline = labels.get("pipeline", "Unknown pipeline")
        provider = labels.get("provider", "Unknown provider")
        severity = labels.get("severity", "unknown")

        summary = annotations.get("summary", "")
        description = annotations.get("description", "")

        message = (
            f"🚨 **{alert_name}**\n\n"
            f"**Status:** {status}\n"
            f"**Pipeline:** `{pipeline}`\n"
            f"**Provider:** `{provider}`\n"
            f"**Severity:** `{severity}`\n\n"
            f"**Summary:** {summary}\n"
            f"**Details:** {description}"
        )

        messages.append(message)

    for message in messages:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=10
        )
        response.raise_for_status()

    return {"status": "sent"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
