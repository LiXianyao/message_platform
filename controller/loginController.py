# -*- coding: utf-8 -*-
from models.users import Users
from database import db_session
class loginController:
    def check_login(self,username,passwd):
        users = Users.query.filter(Users.username==username).first()
        print users
        if users==None:#没有找到用户名为给定值的元组
            return False
        if users.passwd != passwd:
            return False
        return True

    def register(self,username,passwd):
        if(len(username)==0):
            resp = {"message": "用户名不可为空", "successed": False}
            return resp
        #查证是否已存在
        users = Users.query.filter(Users.username==username).first()
        print users
        if users!=None:#没有找到用户名为给定值的元组
            resp = {"message": "用户已存在，请重试", "successed": False}
            return resp

        #插入数据库
        newuser = Users(username,passwd)
        db_session.add(newuser)
        db_session.flush()
        return {"message": "注册成功！", "successed": True}