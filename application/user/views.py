from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user,login_required
from application.auth.models import User
from application.user.forms import UserEditForm

@app.route("/user/edit", methods = ["GET", "POST"])
@login_required
def edit_user():
    form = UserEditForm(request.form)

    if request.method == 'POST' and form.validate():
        #user = User.query.filter_by(username=form.username.data).first()

        commit = 0
        u = User.query.get(current_user.id)
        if form.name.data:
            u.name = form.name.data
            commit = 1
        else:
            u.name = current_user.name
        if form.password2.data:
            u.set_password(form.password2.data)
            commit = 1
        
        if commit:
            db.session.commit()
        return redirect(url_for('booking_index'))
    else:
        return render_template('user/edit_user.html', form=form)


    return render_template('user/edit_user.html', form=form)