from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from database import init_db
from routes.auth import auth_bp
from routes.text_generation import text_bp

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    init_db(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(text_bp)

    @app.route("/")
    def home():
        return {"message": "Welcome to AI-Powered Text Generation API"}
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
