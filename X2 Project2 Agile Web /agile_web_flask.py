from app import app, db
from app.models import User, Answer, Question, Qsrelation, QuizSet, init

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Answer': Answer,
        'Question': Question,
        'Qsrelation':Qsrelation,
        'QuizSet': QuizSet
    }

if __name__=="__main__":
    #init()
    app.run(debug=True)