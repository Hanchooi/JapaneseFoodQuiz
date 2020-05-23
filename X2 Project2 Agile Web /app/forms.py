from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.models import User
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
    retypePassword = PasswordField('Retype Password:', validators=[DataRequired()])
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
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, userID):
        user = User.query.filter_by(userID=userID.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
