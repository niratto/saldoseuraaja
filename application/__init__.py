from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy
import os

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

# Autentikaatio, käyttäjänhallinta
from application.auth import models
from application.auth import views

# Reksiteröinti
from application.register import views

# Booking, eli sovelluksen "pääsivu"
from application.booking import views

# admin-osuus
from application.admin import views

# Käyttäjän editointi (booking-sivulta)
from application.user import views

# Rahalähteen lisääminen
from application.moneysource import models
from application.moneysource import views

# transaktion (meno/tulo) lisääminen
from application.transaction import models
from application.transaction import views

# saldon lisääminen
from application.saldo import models
from application.saldo import views

# budjetin lisääminen
from application.budget import views
from application.budget import models

# reporttien lisääminen
from application.reporting import views

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
