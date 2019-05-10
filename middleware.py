# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask,request,render_template,url_for,session,escape,redirect


#登录检查中间件
def LoinRequired(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        #若session中不含有username字段，则认为没有登录，重定向到登陆页面
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return decorated_function

def hasLogged(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'username' in session:
            #用户已登录，重定向到主页
            return redirect(url_for('welcome'))
        return f(*args,**kwargs)
    return decorated_function