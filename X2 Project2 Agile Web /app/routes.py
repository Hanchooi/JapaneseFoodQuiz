from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, AdminForm, SignUpForm, PasswordForm, NameForm


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
        flash("Login requested for Admin ID {}, remember_me={}, Password {}".format(
            form.userID.data, form.remember_me.data, form.password.data
        ))
        return redirect('/manage_quiz')

    return render_template('admin_login.html', form=form)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    form = LoginForm()

    if form.validate_on_submit():
        flash("Login requested for User ID {}, remember_me={}, Password {}".format(
            form.userID.data, form.remember_me.data, form.password.data
        ))
        return redirect('/user_page')

    return render_template('user_login.html', form=form)


@app.route('/user_register', methods=['GET', 'POST'])
def user_signUp():

    form = SignUpForm()

    if form.validate_on_submit():
        flash("Sign Up requested from userID {}, remember_me={}, Password {}, Display Name{} ".format(
            form.userID.data, form.remember_me.data, form.password.data, form.displayName.data
        ))
        return redirect('/user_page')

    return render_template('user_register.html', form=form)


@app.route('/user_change_password', methods=['GET', 'POST'])
def user_change_password():

    form = PasswordForm()

    if form.validate_on_submit():
        flash("Password change requested from userID {}, remember_me={} to new password {}".format(
            form.userID.data, form.remember_me.data, form.newPassword.data
        ))
        return redirect('/user_page')

    return render_template('change_password.html', form=form)


@app.route('/admin_change_password', methods=['GET', 'POST'])
def admin_change_password():

    form = PasswordForm()

    if form.validate_on_submit():
        flash("Password change requested from adminID {}, remember_me={} to new password {}".format(
            form.userID.data, form.remember_me.data, form.newPassword.data
        ))
        return redirect('/manage_quiz')

    return render_template('change_password.html', form=form)

@app.route('/admin_change_name', methods=['GET', 'POST'])
def admin_change_name():

    form = NameForm()

    if form.validate_on_submit():
        flash("Name change requested from adminID {} to newDisplayName {}".format(
            form.userID.data, form.newDisplayName.data
        ))
        return redirect('/manage_quiz')

    return render_template('change_name.html', form=form)

@app.route('/user_change_name', methods=['GET', 'POST'])
def user_change_name():

    form = NameForm()

    if form.validate_on_submit():
        flash("Name change requested from userID {} to newDisplayName {}".format(
            form.userID.data, form.newDisplayName.data
        ))
        return redirect('/user_page')

    return render_template('change_name.html', form=form)