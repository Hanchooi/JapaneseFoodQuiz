from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from app.models import User, QuizSet
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):

    userID = StringField('User ID:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    
    userID = StringField('User ID:', validators=[DataRequired()])
    displayName = StringField('Display Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    retypePassword = PasswordField('Retype Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class AdminForm(FlaskForm):

    userID = StringField('Admin ID:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')



class PasswordForm(FlaskForm):
    
    userID = StringField('ID:', validators=[DataRequired()])
    oldPassword = PasswordField('Old Password:', validators=[DataRequired()])
    newPassword = PasswordField('New Password:', validators=[DataRequired()])
    retypePassword = PasswordField('Retype Password:', validators=[DataRequired(), EqualTo('newPassword')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Change Password')


class NameForm(FlaskForm):
    userID = StringField('ID:', validators=[DataRequired()])    
    newDisplayName = StringField('New Display Name:', validators=[DataRequired()])
    submit = SubmitField('Change Name')

class RegistrationForm(FlaskForm):
    userID = StringField('UserID', validators=[DataRequired()])
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
    submit = SubmitField('upload')

class EditQuizForm(FlaskForm):
    quizSetId = StringField('Quiz Set ID', validators=[DataRequired()])
    quizName = StringField('Quiz Name', validators=[DataRequired()])
    quizDescription = StringField('Quiz Description ', validators=[DataRequired()])
    picture = FileField('select picture',  validators=[DataRequired()])
    submit = SubmitField('upload')

class QuestionFrom(FlaskForm):

    quizSetId = StringField('quiz set id :', validators=[DataRequired('')])
    question = StringField('Question :', validators=[DataRequired()])
    choiceA = StringField('choice A :', validators=[DataRequired()])
    choiceB = StringField('choice B :', validators=[DataRequired()])
    choiceC = StringField('choice C :')
    choiceD = StringField('choice D :')
    submit = SubmitField('upload')

class EditQuestionForm(FlaskForm):
    
    quizSetId = StringField('Quiz Set id :', validators=[DataRequired('')])
    questionID = StringField('Question ID :', validators=[DataRequired()])
    question = StringField('Question :', validators=[DataRequired()])
    choiceA = StringField('choice A :', validators=[DataRequired()])
    choiceB = StringField('choice B :', validators=[DataRequired()])
    choiceC = StringField('choice C :')
    choiceD = StringField('choice D :')
    submit = SubmitField('upload')
class AnswerForm(FlaskForm):
    submit = SubmitField('Next')

