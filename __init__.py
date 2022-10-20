from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='assets')
app.secret_key = 'TinyJar Production'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root@127.0.0.1/tiny_jar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from finance_track import routes
