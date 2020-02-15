"""2020/02/13 20:49
献给燕燕的情人节礼物.
"""

import datetime
import os
import secrets

import ujson
from flask import Flask, Response, request
from flask_cors import CORS

SECRET_KEY = secrets.token_hex()
USERNAME = os.environ.get("WY_USERNAME", "lingshiyun")
PASSWORD = os.environ.get("WY_PASSWORD", "wuyan")

# Flask app
app = Flask(__name__)
CORS(app)


@app.route("/api/wy/login/", methods=["POST"])
def login():
    """处理登陆"""
    if request.method == 'POST':
        raw_data = request.get_data().decode()
        data = ujson.loads(raw_data)
        username = data.get("username", None)
        password = data.get("password", None)
        if username == USERNAME and password == PASSWORD:
            return {"code": 200, "message": "Ok", "data": {}}
    return {"code": 403, "message": "Forbidden", "data": {}}


@app.route("/api/wy/load/<string:type>/", methods=["GET"])
def load(type: str):
    """加载数据"""
    try:
        with open("storage.json", "r+") as f:
            data = ujson.load(f)
        if type == "all":
            return {"code": 200, "message": "Ok", "data": data}
        return {"code": 200, "message": "Ok", "data": {type: data[type]}}
    except Exception:
        return {"code": 404, "message": "Not Found", "data": {"todo": [], "completed": []}}


@app.route("/api/wy/add/<string:type>/", methods=["POST"])
def add(type: str):
    """更新数据"""
    try:
        raw_data = request.get_data().decode()
        if not raw_data:
            raise ValueError
        data = raw_data
        # data = ujson.loads(raw_data)
        with open("storage.json", "r") as f:
            origin_data = ujson.load(f)
            origin_data[type].append(data)
        with open("storage.json", "w+") as f:
            ujson.dump(origin_data, f)
        return {"code": 200, "message": "Ok", "data": origin_data}
    except Exception:
        return {"code": 400, "message": "Bad Request", "data": {"todo": [], "completed": []}}


@app.route("/api/wy/move/<string:type>/", methods=["POST"])
def move(type: str):
    """更新数据"""
    try:
        raw_data = request.get_data().decode()
        if not raw_data:
            raise ValueError
        data = raw_data
        # data = ujson.loads(raw_data)
        with open("storage.json", "r") as f:
            origin_data = ujson.load(f)
            if type == "completed":
                origin_data["todo"].remove(data)
            elif type == "todo":
                origin_data["completed"].remove(data)

            origin_data[type].append(data)
        with open("storage.json", "w+") as f:
            ujson.dump(origin_data, f)
        return {"code": 200, "message": "Ok", "data": origin_data}
    except Exception:
        return {"code": 400, "message": "Bad Request", "data": {"todo": [], "completed": []}}


@app.route("/api/wy/delete/<string:type>/", methods=["POST"])
def delete(type: str):
    """删除某条数据"""
    try:
        raw_data = request.get_data().decode()
        if not raw_data and raw_data != 0:
            raise ValueError
        data = int(raw_data)
        # data = ujson.loads(raw_data)
        with open("storage.json", "r") as f:
            origin_data = ujson.load(f)
            origin_data[type].pop(data)
        with open("storage.json", "w+") as f:
            ujson.dump(origin_data, f)
        return {"code": 200, "message": "Ok", "data": data}
    except Exception:
        return {"code": 400, "message": "Bad Request", "data": {}}
