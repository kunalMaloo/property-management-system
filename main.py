from flask import Flask
import os
import secrets
from application.config import LocalDevelopmentConfig
from application.database import db

app = None


def build_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv("ENV", "development") == "production":
        raise Exception("production config is not setup")
    else:
        print("Starting Local Deveopment Enviroment")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret
    return app


app = build_app()

# from application.controllers import *
from application.controllers.indexControllers import *
from application.controllers.adminControllers import *
from application.controllers.agentControllers import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", debug=True)
