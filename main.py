from flask import Flask
from dataclasses import db
from routes import recordPages

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["database"] = db

app.register_blueprint(recordPages)

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run("0.0.0.0", 2000, debug=True)
