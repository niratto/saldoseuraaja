from application import app, db
from flask_login import login_required, current_user
from flask import redirect, render_template, request, url_for
from application.booking.forms import BookingForm

@app.route("/booking", methods=["GET"])
@login_required
def booking_index():
    return render_template("booking/index.html")
