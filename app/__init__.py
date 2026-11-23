from flask import Flask, jsonify


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def health():
        return jsonify({
            "application": "SecureBank",
            "status": "running"
        })

    return app