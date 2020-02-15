import os
import datetime

JWT_SECRET_KEY = os.urandom(32)


def configure_jwt(jwt):
    """
    configure handlers to flask_jwt
    """

    @jwt.authentication_handler
    def authenticate(account):
        """ 
        实现账号的验证逻辑，并返回自定义数据，该数据会在下面identity函数中通过payload['identity']
        取到
        """
        raw_token = {
            "user": account,
            "login": datetime.datetime.now()
        }
        return raw_token

    @jwt.identity_handler
    def identity(payload):
        """ 
        接受一个 payload 对象作为参数，并返回根据payload['identity']的值查找对应的信息。返回 
        的数据, current_identity(from jwt import current_identiy)会用到
        """
        pass
