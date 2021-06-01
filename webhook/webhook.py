from flask import Blueprint, request, current_app, redirect
import json

webhook = Blueprint("webhook", __name__)


@webhook.route("/webhook", methods=["POST"])
def order():
    event = request.json
    current_app.logger.info("================= WEBHOOK =================")
    current_app.logger.info(f"Event: {event['key']}")
    current_app.logger("raw data:{}".format(event))
    current_app.logger.info("================= END WEBHOOK =================")
    return json.dumps({"success": True}), 500, {"ContentType": "text/html", "charset": "ISO-8859-1"}
