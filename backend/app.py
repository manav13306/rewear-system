# ReWear Clothing System - Flask Application
# Main application factory and initialization

import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from database import init_mongodb

load_dotenv()

jwt = JWTManager()


def _parse_origins(raw_origins):
    if not raw_origins:
        return [
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def create_app(config_name=None):
    """Application factory function."""
    app = Flask(__name__)

    env_name = config_name or os.getenv("FLASK_ENV", "development").lower()
    is_production = env_name == "production"

    app.config["MONGODB_URL"] = os.getenv("MONGODB_URL", "mongodb://localhost:27017/rewear")
    app.config["DEBUG"] = not is_production

    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if is_production and not jwt_secret:
        raise RuntimeError("JWT_SECRET_KEY must be set in production")

    app.config["JWT_SECRET_KEY"] = jwt_secret or "dev-only-change-this-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    init_mongodb(app)
    jwt.init_app(app)

    cors_origins = _parse_origins(os.getenv("CORS_ORIGINS"))
    CORS(
        app,
        resources={r"/api/*": {"origins": cors_origins}},
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type", "Authorization"],
    )

    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.impact import impact_bp
    from routes.items import items_bp
    from routes.messages import messages_bp
    from routes.orders import orders_bp
    from routes.requests import requests_bp
    from routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(items_bp, url_prefix="/api/items")
    app.register_blueprint(requests_bp, url_prefix="/api/requests")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
    app.register_blueprint(impact_bp, url_prefix="/api/impact")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(messages_bp, url_prefix="/api/messages")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"message": "Internal server error"}), 500

    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False), host="0.0.0.0", port=5000)
