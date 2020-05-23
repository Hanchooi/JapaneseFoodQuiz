from app import db

# Initializing basic user info


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

    # Printing out which user is current
    def __repr__(self):
        return '<UserId {0}, email {1}>'.format(self.userID, self.email)

class QuizSet(db.Model):
    __table_args__ = {'extend_existing': True}
    quizSetID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    picture = db.Column(db.String(200))

    def __init__(self, title, picture):
        self.title = title
        self.picture = picture

    def __repr__(self):
        return '<QuizsetID {0}>'.format(self.quizSetID)


class Answer(db.Model):
    __table_args__ = {'extend_existing': True}
    answerID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    quizSetID = db.Column(db.Integer, db.ForeignKey('quizSet.quizSetID'))
    highScore = db.Column(db.Integer)

    def __init__(self, userID, quizSetID, highScore):
        self.userID = userID
        self.quizSetID = quizSetID
        self.highScore = highScore

    def __repr__(self):
        return '<AnswerID {0}, userID {1}>'.format(self.answerID, self.userID)


class Question(db.Model):
    __table_args__ = {'extend_existing': True}
    questionID = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    choiceA = db.Column(db.String(100))
    choiceB = db.Column(db.String(100))
    choiceC = db.Column(db.String(100))
    choiceD = db.Column(db.String(100))
    correctAnswer = db.Column(db.String(2))

    def __init__(self, question, choiceA, choiceB, choiceC, choiceD, correctAnswer):
        self.question = question
        self.choiceA = choiceA
        self.choiceB = choiceB
        self.choiceC = choiceC
        self.choiceD = choiceD
        self.correctAnswer = correctAnswer

    def __repr__(self):
        return '<questionID {0},  correctAnswer {1}>'.format(self.questionID, self.correctAnswer)



class Qsrelation(db.Model):
    __table_args__ = {'extend_existing': True}
    qurelationID = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'))

    def __init__(self, questionID):
        self.questionID = questionID

    def __repr__(self):
        return '<QsrelationID {0}>'.format(self.qurelationID)

if __name__=="__main__":
    db.cle
    db.create_all()
    admin = User('min@example.com', "123")
    db.session.add(admin)

    question = Question('1',"A",'B','C','D',"A")
    db.session.add(question)
    db.session.commit()

    users = User.query.all()
    print(users)

    questions = Question.query.all()
    print(questions)
