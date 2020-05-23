from flask import render_template, flash, redirect, url_for,request
from app import app, db
from app.forms import LoginForm, AdminForm, SignUpForm, PasswordForm, NameForm, RegistrationForm, UploadQuizFrom
from app.models import User, QuizSet
from flask_login import login_user, logout_user, current_user, login_required


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

@login_required
@app.route('/manage_quiz')
def manage_quiz():
    return render_template('manage_quiz.html')


@login_required
@app.route('/manage_user')
def manage_user():
    return render_template('manage_user.html')


@login_required
@app.route('/upload_question_set')
def upload_question_set():
    return render_template('upload_question_set.html')


@login_required
@app.route('/upload_quiz',methods=['GET', 'POST'])
def upload_quiz():
    form = UploadQuizFrom()
    if form.validate_on_submit():
        file = request.files['file'].read()
        quizSet = QuizSet(name=form.quizName.data, description=form.quizDescription.data, picture=file)
        db.session.add(quizSet)
        db.session.commit()
    return render_template('upload_quiz.html')


@login_required
@app.route('/user_page')
def user_page():
    user = current_user
    if user.status == "admin":
        return render_template('user_page.html', username=current_user.name)
    else:
        return render_template('user_page.html', username=current_user.name)


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.userID.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid userID or password")
            return redirect(url_for('user_login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/manage_user', username=current_user.name)

    return render_template('admin_login.html', form=form)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.userID.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid userID or password")
            return redirect(url_for('user_login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/user_page')

    return render_template('user_login.html', form=form)


@app.route('/user_register', methods=['GET', 'POST'])
def user_signUp():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(id=form.userID.data, name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('user_login'))
    return render_template('user_register.html', title='Register', form=form)

@login_required
@app.route('/user_change_password', methods=['GET', 'POST'])
def user_change_password():

    form = PasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.set_password(form.password.data)
        db.session.commit()
        return redirect('/user_page')

    return render_template('change_password.html', form=form)

@login_required
@app.route('/admin_change_password', methods=['GET', 'POST'])
def admin_change_password():

    form = PasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.set_password(form.password.data)
        db.session.commit()
        return redirect('/manage_quiz')

    return render_template('change_password.html', form=form)

@login_required
@app.route('/admin_change_name', methods=['GET', 'POST'])
def admin_change_name():

    form = NameForm()

    if form.validate_on_submit():
        flash("Name change requested from adminID {} to newDisplayName {}".format(
            form.userID.data, form.newDisplayName.data
        ))
        return redirect('/manage_quiz')

    return render_template('change_name.html', form=form)

@login_required
@app.route('/user_change_name', methods=['GET', 'POST'])
def user_change_name():

    form = NameForm()
    if form.validate_on_submit():
        user = current_user
        user.name = form.newDisplayName.data
        db.session.commit()
        return redirect('/user_page')

    return render_template('change_name.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
