from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from ServiceWebsite import app, db, bcrypt
from ServiceWebsite.forms import RegistrationForm, LoginForm, CommentForm
from ServiceWebsite.models import User, Comment
from flask_login import login_user, current_user, logout_user

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash("Comment sent. Thank you for your feedback.", 'success')
        return redirect(url_for('home'))

    comments = Comment.query.all()
    return render_template("home.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Account Created for {form.name.data}", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for("home"))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))