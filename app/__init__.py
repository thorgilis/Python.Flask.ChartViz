from flask import Flask

def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app