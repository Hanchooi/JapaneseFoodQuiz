from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


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


@app.route('/user_login')
def user_login():
    return render_template('user_login.html')


@app.route('/user_page')
def user_page():
    return render_template('user_page.html')


@app.route('/user_register')
def user_register():
    return render_template('user_register.html')


@app.route('/admin')
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
            form.username.data, form.remember_me.data
        ))
        return redirect('/index')

    return render_template('login.html', form=form)
