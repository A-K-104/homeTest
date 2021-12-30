from flask_session import Session
from flask import Flask, request, session, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from classes.status import Status
from classes.transition import Transition

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_BINDS'] = {'broadcast': 'sqlite:///data.db'}
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sess = Session(app)


# db = SQLAlchemy(app)


# class Users(db.Model):
#     # to init db in terminal type: python ->from app import db->db.create_all()-> exit(). and you are set!
#     email = db.Column(db.String(200), primary_key=True)
#     password = db.Column(db.String(200), nullable=False)
#     twilioAuthToken = db.Column(db.String(200), nullable=True)
#     twilioAccountSid = db.Column(db.String(200), nullable=True)
#     twilioMessagingServiceSid = db.Column(db.String(200), nullable=True)
#     blacklist = db.Column(db.JSON)
#     generalList = db.Column(db.JSON)
#     expiredList = db.Column(db.JSON)
#     expiringList = db.Column(db.JSON)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Name %r>' % self.id
#
#
# @app.before_first_request
# def create_tables():
#      db.create_all()


@app.route('/', methods=['GET', 'POST'])
def baseRoute():
    return redirect("/home")


@app.route('/home', methods=['GET', 'POST'])
def home():
    statuses = [Status("name")]
    transitions = [Transition("name", "user", "to user")]
    if request.method == "POST":
        if request.form.__contains__('name'):
            statuses.append(Status(request.form['name']))
        elif request.form.__contains__('transition'):
            statuses.append(Status(request.form['name']))
    return render_template("home.html", statuses=statuses, transitions=transitions)


if __name__ == "__main__":
    app.run()
