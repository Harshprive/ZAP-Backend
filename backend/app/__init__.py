from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import mongo, jwt, init_fs
from gridfs import GridFS
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)
    init_fs(app)


    # Register Blueprints
    from app.routes.user_routes import user_bp
    from app.routes.provider_routes import provider_bp
    from app.routes.matching_routes import matching_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.location_routes import location_bp 

  

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(provider_bp, url_prefix="/api/provider")
    app.register_blueprint(matching_bp, url_prefix="/api/match")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(location_bp, url_prefix="/api/location")

    global fs
    fs = GridFS(mongo.db)

    return app
