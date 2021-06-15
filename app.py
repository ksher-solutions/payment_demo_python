from flask import Flask
from config import Config
from store.store import store
from payment.checkout import checkout
from webhook.webhook import webhook
from flask_talisman import Talisman
from logging.config import dictConfig



def create_app(config_class=Config):
    app = Flask(__name__)
    app.logger.setLevel('INFO')
    app.config.from_object(config_class)
    app.register_blueprint(store)
    app.register_blueprint(checkout)
    app.register_blueprint(webhook)

    # Adding Content Security Policy to load all content either locally or from heroku
    Talisman(
        app,
        content_security_policy={
            "default-src": "'unsafe-inline' 'self' *.amazonaws.com *.herokuapp.com *googleapis.com *.ksher.com"
        },
    )

    return app

