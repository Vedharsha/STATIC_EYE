from flask import Flask
from app.routes import main
from app.database import db, init_db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        init_db(app)

    app.register_blueprint(main)

    return app