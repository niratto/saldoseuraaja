from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.moneysource.forms import MoneysourceForm
from application.moneysource.models import Moneysource

@app.route("/source", methods=["GET","POST"])
@login_required
def moneysource():
    return render_template("moneysource/moneysource.html", sources = Moneysource.query.filter_by(acc_id_fk=current_user.id))

@app.route("/source/remove/<source_id>/", methods=["POST"])
@login_required
def remove_moneysource(source_id):
    ms = Moneysource.query.get(source_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    db.session().delete(ms)
    db.session().commit()

    flash("Rahalähde id:llä " + source_id + " on nyt poistettu")
    return redirect(url_for("moneysource"))

@app.route("/source/add/", methods = ["GET", "POST"])
@login_required
def add_moneysource():
    form = MoneysourceForm(request.form)
    
    if request.method == 'POST' and form.validate():
        m = Moneysource(form.name.data , form.info.data)
        m.acc_id_fk = current_user.id
        db.session().add(m)
        db.session.commit()
    
        return redirect(url_for('moneysource'))

    return render_template("moneysource/add_moneysource.html", form = form)

@app.route("/source/modify/<int:source_id>", methods = ["GET","POST"])
@login_required
def modify_moneysource(source_id):
    
    ms = Moneysource.query.get(source_id)
    
    if ms:
        form = MoneysourceForm(formdata=request.form)
        if request.method == 'POST' and form.validate():
            ms.ms_id_pk = source_id
            ms.ms_name = form.name.data
            ms.ms_extrainfo = form.info.data
            ms.acc_id_fk = current_user.id
            
            db.session.commit()
            # save edits
            #save_changes(album, form)
            flash('JESS!' + str(source_id) + ' ' + str(current_user.id))
            return redirect(url_for('moneysource'))
        else:
            form.name.data = ms.ms_name
            form.info.data = ms.ms_extrainfo
            return render_template('moneysource/modify_moneysource.html', form=form, source_id=source_id)
    else:
        return 'Error loading #{id}'.format(id=id)
