"""
This __init__.py file is apparently useful for app creation in terms of separation of concerns,
and it normally used to create an app factory pattern.
"""

from flask import Flask


def create_app():
    """
    Docstring goes here.
    :return:
    """
    app = Flask(__name__)

    from .routes import bp
    app.register_blueprint(bp)

    return app
