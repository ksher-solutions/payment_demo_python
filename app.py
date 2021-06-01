from flask import Flask
from config import Config
from store.store import store
from payment.checkout import checkout
from webhook.webhook import webhook
from flask_talisman import Talisman
from logging.config import dictConfig

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })


def create_app(config_class=Config):
    app = Flask(__name__)
    app.logger.setLevel('INFO')
    app.config.from_object(config_class)
    app.register_blueprint(store)
    app.register_blueprint(checkout)
    app.register_blueprint(webhook)

    # Adding Content Security Policy to load all content either locally or from omise.co.
    # Talisman(
    #     app,
    #     content_security_policy={
    #         "default-src": "'unsafe-inline' 'self' *.amazonaws.com *.omise.co *googleapis.com"
    #     },
    # )

    return app
