from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    userID = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(128))
    name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def __init__(self, userId, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.userID = userId

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Printing out which user is current
    def __repr__(self):
        return '<UserId {0}, email {1}>'.format(self.userID, self.email)

@login.user_loader
def load_user(userID):
    return User.query.get(userID)


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
    quizSetID = db.Column(db.Integer)
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
    db.drop_all()
    db.create_all()
    user1 = User('Jason', '22993156', '22993156@uwa.studemt.edu.au', "jason001")
    user2 = User('Ben', '22993546', '22993546@uwa.student.edu.au', "bem001")
    db.session.add_all([user1, user2])
    db.session.commit()


    question1 = Question('What is Sake made of',"A. Corn",'B. Wheat','C. Potato','D. Rice', "D")
    question2 = Question('where have the famous Sake in Japan.', "A Tokyo", 'B. HokkaidoRegion', 'C.Fukui', 'D.Aomori', "B")
    question3 = Question('The roots of Japanese Sake goes back to B.C. 500~? and is said to be made by "chew and spit" method, where the ingredient (raw rice) is once chewed and spit back by a human in a container to be fermented into Sake.',
                         "A.800", 'B.1000', 'C.1500', 'D.2000',"B")
    question4 = Question('Japanese Sake is largely grouped into two types, Junmai-shu type and a Honjozo-shu type.The characteristic that defines sake into one of these categories is:', "A. The maker of the sake", 'B. The type of rice and water used for the sake', 'C. The taste', 'D. Made with or without additional alcohol (distilled alcohol) during the production',
                         "D")
    question5 = Question('Japanese Sake is the most consumed alcoholic beverage in Japan', "A.True", 'B.False', '', '', "A")
    db.session.add_all([question1, question2, question3, question4, question5])
    db.session.commit()

    users = User.query.all()
    print(users)

    questions = Question.query.all()
    print(questions)