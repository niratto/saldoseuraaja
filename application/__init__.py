from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
	# Käytetään saldoseuraaja.db-nimistä SQLite-tietokantaa. Kolme vinoviivaa
	# kertoo, tiedosto sijaitsee tämän sovelluksen tiedostojen kanssa
	# samassa paikassa
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///saldoseuraaja.db"
	# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
	app.config["SQLALCHEMY_ECHO"] = True

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

from application import views

from application.auth import models
from application.auth import views

from application.register import models
from application.register import views

from application.booking import models
from application.booking import views

# kirjautuminen
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Luodaan lopulta tarvittavat tietokantataulut
try:
	db.create_all()
except:
	pass
