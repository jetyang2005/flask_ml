#-*- coding: UTF-8 -*-
import jwt, datetime, time,base64
from flask import jsonify
from app.users.model import Users
from .. import config
from .. import common

class Auth():
    @staticmethod
    def encode_auth_token(user_id, user_name):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            login_time = int(time.time())
            lens = len(config.SECRET_KEY)
            lenx = lens - (lens % 4 if lens % 4 else 4)
            secret = base64.decodestring(config.SECRET_KEY[:lenx])
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'userid': user_id,
                'sub': user_name,
                'audience': 'AUDIENCE_WEB',
                'created': login_time

            }
            token =  jwt.encode(
                payload,
                secret,
                algorithm='HS512'
            )
            return token
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证audience='AUDIENCE_WEB', algorithms=['HS512'],
            lens = len(config.SECRET_KEY)
            lenx = lens - (lens % 4 if lens % 4 else 4)
            secret = base64.decodestring(bytes(config.SECRET_KEY[:lenx],'gb2312'))
            # secret = base64.decodestring(config.SECRET_KEY)

            payload = jwt.decode(auth_token, secret,  options={'verify_exp': False})
            if ('userid' in payload):
                return payload
            else:
                raise jwt.InvalidTokenError

        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            raise



    def authenticate(self, user_name, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        userInfo = Users.query.filter_by(user_name=user_name).first()
        if (userInfo is None):
            return jsonify(common.falseReturn('', '找不到用户'))
        else:
            if (userInfo.check_password(userInfo.password, password)):
                userInfo.update()
                token = self.encode_auth_token(userInfo.id,userInfo.user_name)
                return jsonify(common.trueReturn(token.decode(), '登录成功'))
            else:
                return jsonify(common.falseReturn('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')

        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = common.falseReturn('', '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Users.query.filter_by(id=payload['userid']).first()
                    if (user is None):
                        result = common.falseReturn('', '找不到该用户信息')
                    else:
                        result = common.trueReturn(user.id, '请求成功')
                else:
                    result = common.falseReturn('', payload)
        else:
            result = common.falseReturn('', '没有提供认证token')
        return result
