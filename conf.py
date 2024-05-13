from flask import Flask, Blueprint, redirect, render_template, request, session
from flask_login import LoginManager, UserMixin,login_user,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError,DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY']="This is secret key, bro!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1945@localhost/db'
auth = Blueprint('auth',__name__,url_prefix="/auth")
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print(type(user_id))
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(),nullable=False,unique=True, index=True)
    password = db.Column(db.Text(),nullable=False)

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer,db.ForeignKey(User.id))
    body = db.Column(db.String())
    date = db.Column(db.DateTime, default = datetime.utcnow)
class Sign(FlaskForm):
    username = StringField("Taxallusingiz",validators=[DataRequired()])
    password = PasswordField("Parolingiz",validators=[DataRequired()])
    submit = SubmitField("Tasdiqlash")

class Login(FlaskForm):
    username = StringField("Taxallusingiz",validators=[DataRequired()])
    password = PasswordField("Parolingiz",validators=[DataRequired()])
    submit =  SubmitField("Tasdiqlash")


