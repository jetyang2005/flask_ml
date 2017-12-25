#-*- coding: UTF-8 -*-
from flask import jsonify, request
from app.users.model import Users
from app.auth.auths import Auth
from .. import common

def init_api(app):
    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = Users(email=email, user_name=user_name, password=password)
        result = user.add(user)
        if user.id:
            returnUser = {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email
            }
            return jsonify(common.trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(common.falseReturn('', '用户注册失败'))


    @app.route('/login', methods=['POST'])
    def login():
        """
        用户登录
        :return: json
        """
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        auth = Auth()
        if (not user_name or not password):
            return jsonify(common.falseReturn('', '用户名和密码不能为空'))
        else:
            return auth.authenticate(user_name, password)


    @app.route('/user', methods=['GET'])
    def get():
        """
        获取用户信息
        :return: json
        """
        auth = Auth()
        result = auth.identify(request)

        if (result['status'] and result['data']):
            user = Users.query.filter_by(id=result['data']).first()
            returnUser = {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email
            }
            result = common.trueReturn(returnUser, "请求成功")
        return jsonify(result)
