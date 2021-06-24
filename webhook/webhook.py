from flask import Blueprint, request, current_app, redirect
import json
from ksherpay import Payment
webhook = Blueprint("webhook", __name__)


@webhook.route("/webhook", methods=["GET"])
def order():
    data = request.json
    args = request.args
    args_data =request.args.to_dict
    api_url = current_app.config.get('KSHER_API_BASE')
    api_token = current_app.config.get('KSHER_API_TOKEN')
    myPayment = Payment(api_url,token=api_token)
    webhook_url = current_app.config.get('STORE_BASE_URL') + '/webhook'
    checkSign = myPayment.order.checkSignature(webhook_url,args_data)
    current_app.logger.info("================= WEBHOOK =================")
    current_app.logger.info("raw args data:{}".format(args))
    current_app.logger.info("raw resp data:{}".format(data))
    current_app.logger.info("checkSign return:{}".format(checkSign))
    current_app.logger.info("================= END WEBHOOK =================")
    return json.dumps({"success": True})
