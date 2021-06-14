from flask import Blueprint, request, current_app, redirect
import json

webhook = Blueprint("webhook", __name__)


@webhook.route("/webhook", methods=["GET"])
def order():
    data = request.json
    args = request.args
    current_app.logger.info("================= WEBHOOK =================")
    current_app.logger.info("raw args data:{}".format(args))
    current_app.logger.info("raw resp data:{}".format(data))
    current_app.logger.info("================= END WEBHOOK =================")
    return json.dumps({"success": True})
