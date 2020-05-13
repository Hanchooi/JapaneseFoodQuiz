from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    
    user = {'username' : "Han"}

    return render_template('index.html', user = user)

    #return "Hello World"

@app.route('/login')
def login():
    
    user = {'username' : "Han"}
    form = LoginForm()

    return render_template('login.html', user = user, form=form)