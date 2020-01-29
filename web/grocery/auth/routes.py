from flask import Blueprint, request, render_template, redirect, url_for, flash
from grocery.auth.forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from grocery.models import Exchange
from grocery.models import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    formlog=LoginForm()
    formreg=RegisterForm()

    if request.method == 'POST':
        # Check if post request is coming from generating new transaction or
        # logging into transaction
        if formlog.validate_on_submit():
            current_exchange = Exchange.query.filter_by(name=formlog.log_name.data).first()
            if not current_exchange:
                flash('Query is Empty!', 'danger')
            flash(current_exchange.code)
            flash(formlog.log_code.data)
            if current_exchange and check_password_hash(current_exchange.code, formlog.log_code.data):
                login_user(current_exchange, remember=True)
                flash('Logged in successfully.', 'success')
                # Retrieve lists of goals in account
                return redirect(url_for('exchange.load'))

        elif formreg.validate_on_submit():
            new_trans = Exchange(
                name=formreg.reg_name.data,
                code=generate_password_hash(formreg.reg_code.data),
                tax=float(formreg.reg_tax.data),
                tip=float(formreg.reg_tip.data)
            )
            db.session.add(new_trans)
            db.session.commit()

            flash('New Transaction created successfully.', 'success')
            return redirect(url_for("auth.login"))

        flash('Wrong Credentials!.', 'danger')
        return redirect(url_for("auth.login"))

    else:
        # It is a GET request
        return render_template("login.html", formlog=formlog, formreg=formreg)

@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current transaction"""
    logout_user()
    formlog = LoginForm()
    formreg = RegisterForm()
    return render_template("login.html", formlog=formlog, formreg=formreg)

