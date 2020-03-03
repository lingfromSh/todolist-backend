import os
# 创建db对象


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get(
        "TODOLIST_SECRET_KEY") or "PXYYD2VRWZezABhho4aVbi/X7dPJdLje6YUQZk+4+oQ="
    # 数据库链接配置:
    # 数据类型://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{os.getcwd()}/main.db"
    # 设置mysql的错误跟踪信息显示
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 打印每次模型操作对应的SQL语句
    SQLALCHEMY_ECHO = True
