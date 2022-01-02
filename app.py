import json

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from classes.Transition import Transition
from classes.status import Status

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'broadcast': 'sqlite:///data.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Status_db(db.Model):
    name = db.Column(db.String(200), primary_key=True)

    def __repr__(self):
        return '{' + f'"name": "{self.name}"' + '}'


class Transition_db(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    from_user = db.Column(db.String(200))
    to_user = db.Column(db.String(200))

    def __repr__(self):
        return '{' + \
               f'"name": "{self.name}",' + \
               f'"from_user": "{self.from_user}",' \
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
    if request.args.__contains__('name'):
        r = Status_db.query.get_or_404(request.args['name'])
        db.session.delete(r)
        trans = Transition_db.query.all()
        for tran in trans:
            if (tran.to_user == request.args['name']) or (tran.from_user == request.args['name']):
                r = Transition_db.query.get_or_404(tran.name)
                db.session.delete(r)
    elif request.args.__contains__('transition'):
        r = Transition_db.query.get_or_404(request.args['transition'])
        db.session.delete(r)
    elif request.args.__contains__('reset'):
        db.session.query(Transition_db).delete()
        db.session.query(Status_db).delete()
    db.session.commit()
    return redirect(f"/home?selected={request.args['selectedIndex']}")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        if request.form.__contains__('name'):
            if db.session.query(Status_db.name).filter_by(name=request.form['name']).first() is None:
                status = Status_db(name=request.form['name'])
                db.session.add(status)
        elif request.form.__contains__('transition'):
            if db.session.query(Transition_db.name).filter_by(name=request.form['transition']).first() is None:
                if request.form['from_user'] != "" and request.form['to_user'] != "":
                    transition = Transition_db(name=request.form['transition'], from_user=request.form['from_user'],
                                               to_user=request.form['to_user'])
                    db.session.add(transition)
        db.session.commit()
    return redirect(f"/home?selected={request.form['selectedIndex']}")


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
    pickedStatus = request.args.get("selected")
    if (pickedStatus == "" or (not statuses.__contains__(pickedStatus)) or (pickedStatus is None)) and len(
            statuses) > 0:
        pickedStatus = statuses[0].name
    return render_template("home.html", statuses=statuses, transitions=transitions,
                           selected=pickedStatus)


if __name__ == "__main__":
    app.run()
