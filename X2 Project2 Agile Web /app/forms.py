from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


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
    
    oldPassword = PasswordField('Old Password:', validators=[DataRequired()])
    newPassword = PasswordField('New Password:', validators=[DataRequired()])
    retypePassword = PasswordField('Retype Password:', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class NameForm(FlaskForm):
    
    nameDisplayName = StringField('New Display Name:', validators=[DataRequired()])
    submit = SubmitField('Change Name')
