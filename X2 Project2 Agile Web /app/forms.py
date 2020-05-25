from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField,IntegerField
from wtforms.validators import DataRequired
from app.models import User, QuizSet
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):

    userID = IntegerField('User ID:', validators=[DataRequired('Integer Input Required')])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AdminForm(FlaskForm):

    userID = IntegerField('Admin ID:', validators=[DataRequired('Integer Input Required')])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')



class PasswordForm(FlaskForm):
    
    userID = IntegerField('ID:', validators=[DataRequired('Integer Input Required')])
    oldPassword = PasswordField('Old Password:', validators=[DataRequired()])
    newPassword = PasswordField('New Password:', validators=[DataRequired()])
    retypePassword = PasswordField('Retype Password:', validators=[DataRequired(), EqualTo('newPassword')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Change Password')


class NameForm(FlaskForm):
    userID = IntegerField('ID:', validators=[DataRequired('Integer Input Required')])    
    newDisplayName = StringField('New Display Name:', validators=[DataRequired()])
    submit = SubmitField('Change Name')

class RegistrationForm(FlaskForm):
    userID = IntegerField('UserID', validators=[DataRequired('Integer Input Required')])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    retypePassword = PasswordField(
        'RetypePassword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_userID(self, userID):
        user = User.query.filter_by(id=userID.data).first()
        if user is not None :
            raise ValidationError('Please use a different Userid.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UploadQuizFrom(FlaskForm):
    quizName = StringField('Quiz Name', validators=[DataRequired()])
    quizDescription = StringField('Quiz Description ', validators=[DataRequired()])
    picture = FileField('select picture',  validators=[DataRequired()])
    submit = SubmitField('Create Quiz Set')

class EditQuizForm(FlaskForm):
    quizSetId = IntegerField('Quiz Set ID', validators=[DataRequired('Integer Input Required')])
    quizName = StringField('Quiz Name', validators=[DataRequired()])
    quizDescription = StringField('Quiz Description ', validators=[DataRequired()])
    picture = FileField('select picture',  validators=[DataRequired()])
    submit = SubmitField('Edit Quiz Set')

class QuestionFrom(FlaskForm):

    quizSetId = IntegerField('quiz set id :', validators=[DataRequired('Integer Input Required')])
    question = StringField('Question :', validators=[DataRequired()])
    choiceA = StringField('choice A :', validators=[DataRequired()])
    choiceB = StringField('choice B :', validators=[DataRequired()])
    choiceC = StringField('choice C :')
    choiceD = StringField('choice D :')
    submit = SubmitField('Add Question')

class EditQuestionForm(FlaskForm):
    
    quizSetId = IntegerField('Quiz Set id :', validators=[DataRequired('Integer Input Required')])
    questionID = StringField('Question ID :', validators=[DataRequired()])
    question = StringField('Question :', validators=[DataRequired()])
    choiceA = StringField('choice A :', validators=[DataRequired()])
    choiceB = StringField('choice B :', validators=[DataRequired()])
    choiceC = StringField('choice C :')
    choiceD = StringField('choice D :')
    submit = SubmitField('Edit Question')
class AnswerForm(FlaskForm):
    submit = SubmitField('Next')

