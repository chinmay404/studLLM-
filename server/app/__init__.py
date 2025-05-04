from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from app.config import Config

# Initialize PyMongo without an app
mongo = PyMongo()
login_manager = LoginManager()
class Config:
    MONGO_URI = "mongodb+srv://openlabETHAdmin:OpenADIMIN@cluster-1.b0byxgb.mongodb.net/your_database_name?retryWrites=true&w=majority"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("MONGO_URI from Flask:", app.config.get("MONGO_URI"))

    # Initialize PyMongo AFTER setting app config
    mongo.init_app(app)

    if mongo.db is None:
        print("❌ PyMongo failed to initialize. Check MONGO_URI or Flask setup.")
    else:
        try:
            mongo.db.command("ping")  # Check connection
            print("✅ MongoDB connected successfully via Flask!")
        except Exception as e:
            print("❌ Error connecting to MongoDB:", e)

    login_manager.init_app(app)
    login_manager.login_view = "auth.google_login"

    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
