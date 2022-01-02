import json

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from classes.Transition import Transition
from classes.status import Status

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'broadcast': 'sqlite:///data.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        return '{' + \
               f'"name": "{self.name}",' +\
               f'"from_user": "{self.from_user}",'\
               + f'"to_user": "{self.to_user}"' + \
               '} '


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def baseRoute():
    return redirect("/home")


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    # print(request.args['name'])
    if request.args.__contains__('name'):
        r = Status_db.query.get_or_404(request.args['name'])
        db.session.delete(r)
    elif request.args.__contains__('transition'):
        r = Transition_db.query.get_or_404(request.args['transition'])
        db.session.delete(r)
    elif request.args.__contains__('reset'):
        # db.session.delete_all()
        db.session.query(Transition_db).delete()
        db.session.query(Status_db).delete()
    db.session.commit()
    return redirect("/home")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        if request.form.__contains__('name'):
            if not db.session.query(Status_db.name).filter_by(name=request.form['name']).first() is not None:
                status = Status_db(name=request.form['name'])
                db.session.add(status)
                db.session.commit()
        elif request.form.__contains__('transition'):
            if not db.session.query(Transition_db.name).filter_by(name=request.form['transition']).first() is not None:
                transition = Transition_db(name=request.form['transition'], from_user=request.form['from_user'],
                                           to_user=request.form['to_user'])
                db.session.add(transition)
                db.session.commit()
    return redirect("/home")


@app.route('/pick', methods=['GET', 'POST'])
def pick():
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
    return render_template("home.html", statuses=statuses, transitions=transitions)


if __name__ == "__main__":
    app.run()
