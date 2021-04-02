from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def config_db(app, db_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.create_all(app=app)
