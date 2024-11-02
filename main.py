from flask import Flask, render_template, request, session, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('', 'school.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0wfLuSSb4LYBf9j0Ck2W3E1I2tCbEHhRnUzU7WBluZc'
db = SQLAlchemy(app)

class User:
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullabele=False)
    email = db.Column(db.String(150), nullabele=False)
    password = db.Column(db.String(128), nullabele=False)
    role = db.Column(db.Integer, default=0)

    def check_password(self, password):
        return check_password_hash(self.password, password)


with app.app_context():
    db.create_all()


# ROUTES ======================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            message = 'Введіть правильний Email!'
        else:
            if user.check_password(password):
                session['user_name'] = user.username
                return redirect('/')

            message = 'Введіть правильний пароль!'

    return render_template('login.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
