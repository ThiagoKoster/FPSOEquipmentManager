from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def config_db(app, db_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_uri
    db.init_app(app)
    db.create_all(app=app)
