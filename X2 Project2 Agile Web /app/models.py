from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(128))
    name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    status = db.Column(db.String)
    last_login = db.Column(db.DATE, nullable=False, default=datetime.now)


    def __init__(self, id, name, email):
        self.name = name
        self.email = email
        self.id = id
        self.status = "student"

    def set_status(self, status):
        self.status = status

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    # Printing out which user is current
    def __repr__(self):
        return '<UserId {0}, email {1}, name {2}> last_login {3}'.format(self.id, self.email, self.name, self.last_login)

@login.user_loader
def load_user(id):
    user = User.query.filter_by(id=(int(id))).first()
    return user


class QuizSet(db.Model):
    __table_args__ = {'extend_existing': True}
    quizSetID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))
    userID = db.Column(db.String)
    status = db.Column(db.String(100))

    def __init__(self, name, description, picture, userID):
        self.name = name
        self.description = description
        self.picture = picture
        self.status = "pending"
        self.userID = userID

    def set_status(self, status):
        self.status = status

    def __repr__(self):
        return '<QuizsetID {0}>'.format(self.quizSetID)


class Answer(db.Model):
    __table_args__ = {'extend_existing': True}
    answerID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    quizSetID = db.Column(db.Integer)
    correctNumber = db.Column(db.String())
    totalNumber = db.Column(db.Integer)

    def __init__(self, userID, quizSetID):
        self.userID = userID
        self.quizSetID = quizSetID
        self.correctNumber = ""
        self.totalNumber = 0

    def __repr__(self):
        return '<AnswerID {0}, userID {1}>'.format(self.answerID, self.userID)


class Question(db.Model):
    __table_args__ = {'extend_existing': True}
    questionID = db.Column(db.Integer, primary_key=True)
    quizSetID = db.Column(db.Integer)
    question = db.Column(db.String(1000))
    choiceA = db.Column(db.String(100))
    choiceB = db.Column(db.String(100))
    choiceC = db.Column(db.String(100))
    choiceD = db.Column(db.String(100))
    correctAnswer = db.Column(db.String(2))

    def __init__(self, quizSetID, question, choiceA, choiceB, choiceC, choiceD, correctAnswer):
        self.quizSetID = quizSetID
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


def init():
    db.drop_all()
    db.create_all()
    admin = User('1111111', 'admin', 'admin@uwa.studemt.edu.au')
    admin.set_password("admin")
    admin.set_status("admin")

    user1 = User('22993156', 'Jason', '22993156@uwa.studemt.edu.au')
    user1.set_password("jason001")

    user2 = User('22993546', 'Ben', '22993546@uwa.student.edu.au')
    user2.set_password("bem001")

    db.session.add_all([admin, user1, user2])
    db.session.commit()
    users = User.query.all()

if __name__=="__main__":
    db.drop_all()
    # result = User.query.all()
    #     # print(result)
    #     # db.session.delete(result)
    #     # db.session.commit()
    # db.drop_all()
    db.create_all()
    # user1 = User('Jason', '22993156', '22993156@uwa.studemt.edu.au', "jason001")
    # user2 = User('Ben', '22993546', '22993546@uwa.student.edu.au', "bem001")
    # db.session.add_all([user1, user2])
    # db.session.commit()
    #
    #
    # question1 = Question('What is Sake made of',"A. Corn",'B. Wheat','C. Potato','D. Rice', "D")
    # question2 = Question('where have the famous Sake in Japan.', "A Tokyo", 'B. HokkaidoRegion', 'C.Fukui', 'D.Aomori', "B")
    # question3 = Question('The roots of Japanese Sake goes back to B.C. 500~? and is said to be made by "chew and spit" method, where the ingredient (raw rice) is once chewed and spit back by a human in a container to be fermented into Sake.',
    #                      "A.800", 'B.1000', 'C.1500', 'D.2000',"B")
    # question4 = Question('Japanese Sake is largely grouped into two types, Junmai-shu type and a Honjozo-shu type.The characteristic that defines sake into one of these categories is:', "A. The maker of the sake", 'B. The type of rice and water used for the sake', 'C. The taste', 'D. Made with or without additional alcohol (distilled alcohol) during the production',
    #                      "D")
    # question5 = Question('Japanese Sake is the most consumed alcoholic beverage in Japan', "A.True", 'B.False', '', '', "A")
    # db.session.add_all([question1, question2, question3, question4, question5])
    # db.session.commit()
    #
    admin = User('1111111', 'admin', 'admin@uwa.studemt.edu.au')
    admin.set_password("admin")
    admin.set_status("admin")

    user1 = User('22993156', 'Jason', '22993156@uwa.studemt.edu.au')
    user1.set_password("jason001")

    user2 = User('22993546', 'Ben', '22993546@uwa.student.edu.au')
    user2.set_password("bem001")

    db.session.add_all([admin, user1, user2])
    db.session.commit()
    users = User.query.all()
    print(users)

    # questions = Question.query.all()
    # print(questions)