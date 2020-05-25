from flask import render_template, flash, redirect, url_for,request
from app import app, db
from app.forms import LoginForm, AdminForm, PasswordForm, NameForm,\
RegistrationForm, UploadQuizFrom,QuestionFrom, AnswerForm, EditQuizForm, EditQuestionForm
from app.models import User, QuizSet, Question, Answer
from flask_login import login_user, logout_user, current_user, login_required
import base64
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/qs')
def qs():
    quizSets = QuizSet.query.filter_by(status="approve").all()
    for quizSet in quizSets:
        quizSet.href = "/qa?index=0&id="+str(quizSet.quizSetID)
        quizSet.picture = "/static/images/"+quizSet.picture
    return render_template('qs.html', quizSets=quizSets, base64=base64)


@app.route('/qa', methods=['GET', 'POST'])
def qa():
    form = AnswerForm()
    quizSetId = int(request.args.get('id'))
    index = request.args.get('index')
    if index is None:
        index = 0
    else:
        index = int(index)
    question = None
    total_count = 0
    quizSet = QuizSet.query.filter_by(quizSetID=quizSetId).first()
    picture = "/static/images/"+quizSet.picture
    next = "/qa?id="+str(quizSetId)
    if quizSetId is not None:
        questions = Question.query.filter_by(quizSetID=quizSetId).all()
        total_count = len(questions)
        if len(questions) > 0:
            if index < len(questions):
                question = questions[index]
                next += "&index="+str(index+1)
            else:
                flash("finish")
    if question is None:
        flash("no question")
        return redirect('/user_page')
    if form.validate_on_submit():
        choice = request.form.get('choice')
        if choice is not None:
            if question is not None:
                user = current_user
                answer = Answer.query.filter_by(userID=user.id, quizSetID=quizSetId).first()
                if answer is None:
                    answer = Answer(user.id, quizSetId)
                    db.session.add(answer)
                record = answer.correctNumber.split(",")
                if choice.lower() == question.correctAnswer.lower():
                    if str(question.questionID) not in record:
                        if record == "":
                            record = str(question.questionID)
                        else:
                            record.append(str(question.questionID))
                answer.totalNumber = total_count
                if len(record) > 0:
                    answer.correctNumber = ",".join(record)
                else:
                    answer.correctNumber = ""
                db.session.commit()
                if index == len(questions)-1:
                    return redirect('/user_page')
                else:
                    return redirect(next)

    return render_template('qa.html', form=form, question=question, index=index, quizSetId=quizSetId, picture=picture, next=next)



@app.route('/manage_quiz')
@login_required
def manage_quiz():
    user = current_user
    if user.name != 'admin':
        return redirect('/admin')
    quizSetIds = []
    quizSets = QuizSet.query.all()
    for quizSet in quizSets:
        quizSetIds.append(quizSet.quizSetID)
        if quizSet.status == "running":
            quizSet.href = "/delete_quiz_set?id="+ str(quizSet.quizSetID)
    questions = Question.query.all()
    show_questions = []
    for question in questions:
        if question.quizSetID in quizSetIds:
            show_questions.append(question)
    return render_template('manage_quiz.html', quizSets=quizSets, questions=show_questions)


@app.route('/delete_quiz_set')
@login_required
def delete_quiz_set():
    user = current_user
    if user.name == 'admin':
        quizSetId = request.args.get('id')
        if quizSetId is not None:
            quizSet = QuizSet.query.filter_by(quizSetID=int(quizSetId)).first()
            if quizSet.status == "pending":
                quizSet.set_status("approve")
            else:
                db.session.delete(quizSet)

            db.session.commit()
    return redirect('/manage_quiz')


@app.route('/update')
def update():
    user = current_user
    if user.name == 'admin':
        userID = request.args.get('id')
        if userID is not None:
            user = User.query.filter_by(id=int(userID)).first()
            if user:
                db.session.delete(user)
                db.session.commit()
    return redirect('/manage_user')


@app.route('/upload_quiz', methods=['GET', 'POST'])
def upload_quiz():
    form = QuestionFrom()
    id = request.args.get("id")
    if id is not None:
        form.quizSetId.data = id
    if form.validate_on_submit():
        quizSetId = form.quizSetId.data
        quizSet = QuizSet.query.filter_by(quizSetID=int(quizSetId))
        if quizSet is None:
            flash("quizSet not exist")
        else:
            choice = request.form.get('choice')
            question = Question(int(form.quizSetId.data), form.question.data, form.choiceA.data,
                                form.choiceB.data, form.choiceC.data, form.choiceD.data, choice)
            db.session.add(question)
            db.session.commit()
    return render_template('upload_quiz.html', form=form)


@app.route('/edit_quiz', methods=['GET', 'POST'])
def edit_quiz():
    form = EditQuestionForm()
    id = request.args.get("id")
    if id is not None:
        form.questionID.data = id
    if form.validate_on_submit():
        quizSetId = form.quizSetId.data
        quizSet = QuizSet.query.filter_by(quizSetID=int(quizSetId))
        if quizSet is None:
            flash("quizSet not exist")
        else:
            choice = request.form.get('choice')
            question = Question.query.filter_by(questionID=int(id)).first()
            if question is not None:
                question.quizSetID = int(form.quizSetId.data)
                question.question = form.question.data
                question.choiceA = form.choiceA.data
                question.choiceB = form.choiceB.data
                question.choiceC = form.choiceC.data
                question.choiceD = form.choiceD.data
                question.correctAnswer = choice
                db.session.commit()
                return redirect('/manage_quiz')
    return render_template('edit_quiz.html', form=form)


@app.route('/manage_user')
@login_required
def manage_user():
    user = current_user
    if user.name != 'admin':
        return redirect('/admin')
    users = User.query.filter(User.name!="admin")
    return render_template('manage_user.html', users=users)


@app.route('/upload_question_set', methods=['GET', 'POST'])
def upload_question_set():
    form = UploadQuizFrom()
    user = current_user
    if form.validate_on_submit():
        file = request.files['picture']
        if not (file and allowed_file(file.filename)):
            flash("Unacceptable format")
        else:
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file.filename))
            file.save(upload_path)
            quizSet = QuizSet(name=form.quizName.data, description=form.quizDescription.data, picture=file.filename, userID=user.id)
            db.session.add(quizSet)
            db.session.commit()
            return redirect('/upload_quiz?id=' + str(quizSet.quizSetID))
    return render_template('upload_question_set.html', form=form)

@app.route('/edit_question_set', methods=['GET', 'POST'])
def edit_question_set():
    form = EditQuizForm()
    user = current_user
    id = request.args.get("id")
    if id is not None:
        form.quizSetId.data = id
    if form.validate_on_submit() and id is not None:
        file = request.files['picture']
        if not (file and allowed_file(file.filename)):
            flash("Unacceptable format")
        else:
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file.filename))
            file.save(upload_path)
            quizSet = QuizSet.query.filter_by(quizSetID=int(id)).first()
            if quizSet is not None:
                quizSet.name = form.quizName.data
                quizSet.description = form.quizDescription.data
                quizSet.picture = file.filename
                db.session.commit()
                return redirect('/manage_quiz')
    return render_template('edit_question_set.html', form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/user_page')
@login_required
def user_page():
    user = current_user
    if user.name == "admin":
        return redirect('/manage_user')
    answers = Answer.query.filter_by(userID=int(user.id)).all()
    show_answers = []
    if answers and len(answers) > 0:
        for answer in answers:
            records= answer.correctNumber.split(",")
            quiz_set = QuizSet.query.filter_by(quizSetID=answer.quizSetID).first()
            if quiz_set:
                score = str(len(records)-1)+"/"+str(answer.totalNumber)
                show = {"quiz_set_id": answer.quizSetID, "name": quiz_set.name, "score": score}
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
        if user.name == 'admin':
            return redirect('/manage_user')
        else:
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



@app.route('/user_change_password', methods=['GET', 'POST'])
@login_required
def user_change_password():

    form = PasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.set_password(form.newPassword.data)
        db.session.commit()
        return redirect('/user_page')

    return render_template('change_password.html', form=form)



@app.route('/admin_change_password', methods=['GET', 'POST'])
@login_required
def admin_change_password():

    form = PasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.set_password(form.password.data)
        db.session.commit()
        return redirect('/manage_quiz')

    return render_template('change_password.html', form=form)



@app.route('/user_change_name', methods=['GET', 'POST'])
@login_required
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
