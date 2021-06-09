from flask import Blueprint, request, current_app, redirect
import json

webhook = Blueprint("webhook", __name__)


@webhook.route("/webhook", methods=["POST"])
def order():
    data = request.json
    current_app.logger.info("================= WEBHOOK =================")
    current_app.logger.info("raw resp data:{}".format(data))
    current_app.logger.info("================= END WEBHOOK =================")
    return json.dumps({"success": True})
