import constance

db = constance.db


class Status:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other


class Status_db(db.Model):
    name = db.Column(db.String(200), primary_key=True)

    def __repr__(self):
        return '{' + f'"name": "{self.name}"' + '}'
