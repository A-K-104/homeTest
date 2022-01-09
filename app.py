from flask import render_template

import constance
from routes.basicRoutsHandling import basic_routs_handling

app = constance.app
db = constance.db
app.register_blueprint(basic_routs_handling)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
