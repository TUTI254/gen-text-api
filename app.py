from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from database import init_db
from routes.auth import auth_bp
from routes.text_generation import text_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and JWT
init_db(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(text_bp)


@app.route("/")
def home():
    return {"message": "Welcome to AI-Powered Text Generation API"}

if __name__ == "__main__":
    app.run(debug=True)
