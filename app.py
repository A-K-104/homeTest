import json

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'broadcast': 'sqlite:///data.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sess = Session(app)

db = SQLAlchemy(app)


class Status_db(db.Model):
    # to init db in terminal type: python ->from app import db->db.create_all()-> exit(). and you are set!
    name = db.Column(db.String(200), primary_key=True)

    def __repr__(self):
        return '{' + f'"name": "{self.name}"' + '}'


class Transition_db(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    from_user = db.Column(db.String(200))
    to_user = db.Column(db.String(200))

    def __repr__(self):
        return '{' + f'"name": "{self.name}",' + f'"from_user": "{self.from_user}",' + f'"to_user": "{self.to_user}"' + '}'


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def baseRoute():
    return redirect("/home")


@app.route('/home', methods=['GET', 'POST'])
def home():
    names = Status_db.query.all()
    trans = Transition_db.query.all()
    statuses = []
    transitions = []
    for name in names:
        temp = json.loads(str(name))
        statuses.append(Status(temp['name']))
    for tran in trans:
        temp = json.loads(str(tran))
        transitions.append(Transition(temp['name'], temp['from_user'], temp['to_user']))
    if request.method == "POST":
        if request.form.__contains__('name'):
            status = Status_db(name=request.form['name'])
            db.session.add(status)
            statuses.append(Status(request.form['name']))
        elif request.form.__contains__('transition'):
            transition = Transition_db(name=request.form['transition'], from_user=request.form['from_user'],
                                       to_user=request.form['to_user'])
            db.session.add(transition)
            transitions.append(Transition(request.form['transition'], request.form['from_user'],
                                          request.form['to_user']))
        db.session.commit()
    return render_template("home.html", statuses=statuses, transitions=transitions)


if __name__ == "__main__":
    app.run()
