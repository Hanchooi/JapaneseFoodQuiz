from flask import render_template, flash, redirect, url_for,request
from app import app, db
from app.forms import LoginForm, AdminForm, SignUpForm, PasswordForm, NameForm,\
RegistrationForm, UploadQuizFrom,QuestionFrom, AnswerForm
from app.models import User, QuizSet, Question, Answer
from flask_login import login_user, logout_user, current_user, login_required
import base64

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/qs')
def qs():
    quizSets = QuizSet.querry.all()
    return render_template('qs.html', quizSets=quizSets, base64=base64)


@app.route('/qa', methods=['GET', 'POST'])
def qa():
    form = AnswerForm()
    quizSetId = request.get_data('id')
    index = request.get_data('index')
    question = None
    total_count = 0
    if quizSetId is not None:
        questions = Question.query.all()
        total_count = len(questions)
        if len(questions) > 0:
            if index is None:
                index = 0
                question = questions[0]
            elif index < len(questions):
                question = questions[index]
    if form.validate_on_submit():
        if question is not None:
            user = current_user
            answer = Answer.query(userID=user.id, quizSetId=quizSetId)
            if answer is None:
                answer = Answer(user.id, quizSetId)
                db.session.add(answer)
                db.session.commit()
            record = answer.correctNumber.split(",")
            if form.answer.data.lower() == question.correctAnswer.lower():
                if str(question.questionID) not in record:
                    record.append(str(question.questionID))
            else:
                if str(question.questionID) not in record:
                    record.remove(str(question.questionID))
            answer.totalNumber = total_count
            if len(record) > 0:
                answer.correctNumber = ",".join(record)
            else:
                answer.correctNumber = ""
            db.session.commit()
    return render_template('qa.html', form=form, question=question, index=index, quizSetId=quizSetId)


@login_required
@app.route('/manage_quiz')
def manage_quiz():
    quizSets = QuizSet.querry.all()
    return render_template('manage_quiz.html', quizSets=quizSets)


@app.route('/delete_quiz_set')
def delete_quiz_set():
    user = current_user
    if user.name == 'admin':
        quizSetId = request.get_data('id')
        if quizSetId is not None:
            quizSet = QuizSet.query.filter(quizSetID=quizSetId).first()
            db.session.delete(quizSet)
            db.session.commit()
    return redirect('/manage_user')

@app.route('/update')
def update():
    user = current_user
    if user.name == 'admin':
        userID = request.get_data('id')
        if userID is not None:
            user = User.query.filter(id=userID).first()
            db.session.delete(user)
            db.session.commit()
    return redirect('/manage_user')


@app.route('/upload_quiz')
def upload_quiz():
    form = QuestionFrom()
    if form.validate_on_submit():
        choice = request.form.get('choice')
        question = Question(int(form.quizSetId.data), form.question.data, form.choiceA.data,
                            form.choiceB.data, form.choiceC.data, form.choiceD.data, choice)
        db.session.add(question)
        db.session.commit()
    return render_template('upload_quiz.html', form=form)


@login_required
@app.route('/manage_user')
def manage_user():
    users = User.query.filter(User.name!="admin")
    return render_template('manage_user.html', users=users)


@app.route('/upload_question_set', methods=['GET', 'POST'])
def upload_question_set():
    form = UploadQuizFrom()
    user = current_user
    if form.validate_on_submit():
        file = request.files['picture'].read()
        quizSet = QuizSet(name=form.quizName.data, description=form.quizDescription.data, picture=file, userID=user.id)
        db.session.add(quizSet)
        db.session.commit()
        return redirect('/user_page')
    return render_template('upload_question_set.html', form=form)


@login_required
@app.route('/user_page')
def user_page():
    user = current_user
    print(user.id)
    answers = Answer.query.all()
    show_answers = []
    if answers and len(answers) > 0:
        for answer in answers:
            if answer.userID != user.id:
                continue
            record = answer.correctNumber.split(",")
            quiz_set = QuizSet.query.filter(quizSetID=answer.quizSetID).first()
            if quiz_set:
                score = str(len(record))+"/"+str(len(answer.totalNumber))
                show = {"quiz_set_id": answer.quizSetID, "name": quiz_set.name, "socre": score}
                show_answers.append(show)
    quiz_sets = QuizSet.query.all()
    show_quizs = []
    if quiz_sets and len(quiz_sets) > 0:
        for quiz_set in quiz_sets:
            if quiz_set.userID != user.id:
                continue
            q_answers = Answer.query.filter_by(quizSetID=int(quiz_set.quizSetID)).all()
            otherNumber = 0
            if q_answers is not None:
                otherNumber = len(q_answers)
            show = {"quiz_set_id": quiz_set.quizSetID, "name": quiz_set.name, "otherNumber": otherNumber}
            show_quizs.append(show)
    if user.status == "admin":
        return render_template('user_page.html', username=current_user.name)
    else:
        return render_template('user_page.html', username=current_user.name, show_answers=show_answers, show_quizs=show_quizs)


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
        return redirect('/manage_user')

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
