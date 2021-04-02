from flask import Flask
from api.restx import api
from api.endpoints.healthcheck import ns_healthcheck


def create_app():
    app = Flask(__name__)

    api.init_app(app)
    api.add_namespace(ns_healthcheck)
    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
