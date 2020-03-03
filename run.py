import datetime
import os
import secrets

from flask import Flask, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import Config

# Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
SECRET_KEY = app.config.get("SECRET_KEY")
# MODELS


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)
    created = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.id = secrets.token_hex(32)
        self.username = username
        self.password = self.hash_password(password)
        self.created = datetime.datetime.now()
        self.last_login = datetime.datetime.now()

    def __repr__(self):
        return f"<User {self.username}-{self.id}>"

    @classmethod
    def hash_password(cls, raw_password):
        """加密密码"""
        return generate_password_hash(password=raw_password)

    def check_password(self, raw_password):
        """检查密码"""
        return check_password_hash(self.password, raw_password)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        print(user.password)
        return user.check_password(password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created": self.created,
            "last_login": self.last_login
        }


class Todo(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(35))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    # FK
    author_id = db.Column(db.String(32), db.ForeignKey(User.id))
    author = db.relationship(User,
                             backref=db.backref('todos', lazy='dynamic'))
    is_finished = db.Column(db.Boolean)

    def __init__(self, title, content, user, is_finished=False):
        self.id = secrets.token_hex(32)
        self.title = title
        self.content = content
        self.author = user
        self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        self.is_finished = is_finished

    def __repr__(self):
        return f"<Todo {self.title}-{self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created": self.created,
            "updated": self.updated,
            "author": self.author.to_dict(),
            "is_finished": self.is_finished
        }


if not os.path.exists("db_created"):
    db.drop_all()
    with open("db_created", "w+") as f:
        f.write("1")
db.create_all()
# MODELS


# API
# =====
# utils
# =====
def get_index(l, elem):
    try:
        return l.index(elem)
    except ValueError:
        return -1

# =====
# API
# =====
@app.route("/todolist/user/register/", methods=["POST"])
def register():
    """处理注册"""
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", None)
        password = data.get("password", None)
        code = data.get("code", None)
        if code != SECRET_KEY:
            return {"code": 406, "message": "Wrong Code", "data": {}}
        if not username or not password:
            return {"code": 406,
                    "message": "请正确输入想要注册的用户名/密码",
                    "data": {"token": secrets.token_hex(32)}}
        user = User(username, password)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {"code": 406, "message": "Duplicated <username>", "data": {}}
        else:
            return {"code": 200, "message": "Register Successfully", "data": {"token": secrets.token_hex(32)}}
    return {"code": 405, "message": "Method Not Allowed", "data": {}}


@app.route("/todolist/user/login/", methods=["POST"])
def login():
    """处理登陆"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username", None)
        password = data.get("password", None)
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return {"code": 200, "message": "Login Successfully", "data": user.to_dict()}
    return {"code": 403, "message": "Forbidden", "data": {}}


@app.route("/todolist/todos/<string:type>/", methods=["GET"])
def load(type: str):
    """加载数据"""
    if type == "todo":
        todos = Todo.query.filter_by(is_finished=False)
        data = [todo.to_dict() for todo in todos]
        return {"code": 200, "message": "Load Successfully", "data": {"todo": data, "count": len(data)}}
    elif type == "finished":
        todos = Todo.query.filter_by(is_finished=True)
        data = [todo.to_dict() for todo in todos]
        return {"code": 200, "message": "Load Successfully", "data": {"todo": data, "count": len(data)}}
    elif type == "all":
        todos = Todo.query.all()
        data = [todo.to_dict() for todo in todos]
        return {"code": 200, "message": "Load Successfully", "data": {"todo": data, "count": len(data)}}
    else:
        return {"code": 406, "message": "Wrong Type", "data": {}}


@app.route("/todolist/todo/", methods=["POST"])
def add():
    """更新数据"""
    data = request.get_json()
    user = User.query.filter_by(username=data["user"]).first()
    if user:
        data["user"] = user
        todo = Todo(**data)
        db.session.add(todo)
        db.session.commit()
        return {"code": 200, "message": "Add Successfully", "data": {"todo": todo.to_dict()}}
    return {"code": 406, "message": "Wrong Input", "data": {"todo": None}}


@app.route("/todolist/todo/<string:id>/", methods=["GET"])
def get(id: str):
    """更新数据"""
    todo = Todo.query.get(id)
    if todo:
        return {"code": 200, "message": "Add Successfully", "data": {"todo": todo.to_dict()}}
    return {"code": 404, "message": "Todo Not Found", "data": {"todo": None}}


@app.route("/todolist/todo/<string:id>/", methods=["DELETE"])
def delete(id: str):
    """删除某条数据"""
    if request.method == "DELETE":
        todo = Todo.query.get(id)
        if todo:
            todo.delete()
            return {"code": 200, "message": "Delete Successfully", "data": {"todo": None}}
        else:
            return {"code": 404, "message": "Todo Not Found", "data": {"todo": None}}
    else:
        return {"code": 405, "message": "Method Not Allowed", "data": {"todo": None}}


# API
