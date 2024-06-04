from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    
    from .consumer.routes import consumer
    from .store.routes import store
    from .webhook.routes import webhook

    app.register_blueprint(consumer)
    app.register_blueprint(store)
    app.register_blueprint(webhook)

    return app