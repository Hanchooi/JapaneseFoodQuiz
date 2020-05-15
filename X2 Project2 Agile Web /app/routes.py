from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, AdminForm, SignUpForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/qs')
def qs():
    return render_template('qs.html')


@app.route('/qa')
def qa():
    return render_template('qa.html')


@app.route('/manage_quiz')
def manage_quiz():
    return render_template('manage_quiz.html')


@app.route('/manage_user')
def manage_user():
    return render_template('manage_user.html')


@app.route('/upload_question_set')
def upload_question_set():
    return render_template('upload_question_set.html')


@app.route('/upload_quiz')
def upload_quiz():
    return render_template('upload_quiz.html')


@app.route('/user_page')
def user_page():
    return render_template('user_page.html')


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    form = AdminForm()

    if form.validate_on_submit():
        flash("Login requested for admin {}, remember_me={}".format(
            form.userID.data, form.remember_me.data
        ))
        return redirect('/manage_quiz')

    return render_template('admin_login.html', form=form)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    form = LoginForm()

    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
            form.userID.data, form.remember_me.data
        ))
        return redirect('/user_page')

    return render_template('user_login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
            form.userID.data, form.remember_me.data
        ))
        return redirect('/index')

    return render_template('login.html', form=form)


@app.route('/user_register', methods=['GET', 'POST'])
def user_signUp():

    form = SignUpForm()

    if form.validate_on_submit():
        flash("Sign Up requested from user {}, remember_me={}".format(
            form.userID.data, form.remember_me.data
        ))
        return redirect('/user_page')

    return render_template('user_register.html', form=form)