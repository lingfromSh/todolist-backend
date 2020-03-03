import fire
import requests
import secrets
import time
import json

proxy = "http://localhost:5000"


def test_register(times: int = 1, delay: int = 0):
    resp_success = 0
    resp_failed = 0
    resp_timecost = 0.0
    for i in range(int(times)):
        start = time.time()
        time.sleep(float(delay)/1000)
        resp = requests.post(f"{proxy}/todolist/user/register/",
                             json={"username": secrets.token_hex(16),
                                   "password": secrets.token_hex(),
                                   "code": "PXYYD2VRWZezABhho4aVbi/X7dPJdLje6YUQZk+4+oQ="})
        if json.loads(resp.content.decode())["code"] == 200:
            resp_success += 1
        else:
            resp_failed += 1
        resp_timecost += time.time()-start
    print("总请求数:", times)
    print("模拟延迟(ms):", delay)
    print("成功请求数:", resp_success)
    print("失败请求数:", resp_failed)
    print("平均请求时间(ms):", resp_timecost/times)


def test_login(times: int = 1, delay: int = 0):
    resp_success = 0
    resp_failed = 0
    resp_timecost = 0.0
    for i in range(int(times)):
        start = time.time()
        time.sleep(float(delay)/1000)
        resp = requests.post(f"{proxy}/todolist/user/login/",
                             json={"username": secrets.token_hex(16),
                                   "password": secrets.token_hex()})
        if json.loads(resp.content.decode())["code"] == 200:
            resp_success += 1
        else:
            resp_failed += 1
        resp_timecost += time.time()-start
    print("总请求数:", times)
    print("模拟延迟(ms):", delay)
    print("成功请求数:", resp_success)
    print("失败请求数:", resp_failed)
    print("平均请求时间(ms):", resp_timecost/times)


def test_add(times: int = 1, delay: int = 0):
    resp_success = 0
    resp_failed = 0
    resp_timecost = 0.0
    for i in range(int(times)):
        start = time.time()
        time.sleep(float(delay)/1000)
        resp = requests.post(f"{proxy}/todolist/todo/",
                             json={"user": "ling",
                                   "title": secrets.token_hex(),
                                   "content": secrets.token_hex(128),
                                   "is_finished": False
                                   })
        if json.loads(resp.content.decode())["code"] == 200:
            resp_success += 1
        else:
            resp_failed += 1
        resp_timecost += time.time()-start
    print("总请求数:", times)
    print("模拟延迟(ms):", delay)
    print("成功请求数:", resp_success)
    print("失败请求数:", resp_failed)
    print("平均请求时间(ms):", resp_timecost/times)


def test_load(times: int = 1, delay: int = 0):
    resp_success = 0
    resp_failed = 0
    resp_timecost = 0.0
    for i in range(int(times)):
        start = time.time()
        time.sleep(float(delay)/1000)
        resp = requests.get(f"{proxy}/todolist/todos/all/")
        if json.loads(resp.content.decode())["code"] == 200:
            resp_success += 1
        else:
            resp_failed += 1
        resp_timecost += time.time()-start
    print("总请求数:", times)
    print("模拟延迟(ms):", delay)
    print("成功请求数:", resp_success)
    print("失败请求数:", resp_failed)
    print("平均请求时间(ms):", resp_timecost/times)


fire.Fire(test_load)
