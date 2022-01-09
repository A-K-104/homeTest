import constance

db = constance.db


class Transition:
    def __init__(self, name: str, from_user: str, to_user: str):
        self.name = name
        self.from_user = from_user
        self.to_user = to_user

    def __eq__(self, other):
        return self.name == other.name


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
