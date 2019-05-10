# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
import json
import commonFunction
from models.users import Users
from models.identities import Identities
from database import db_session
from sqlalchemy import text
import traceback

userManagement = Blueprint('userManagement'
                                  ,__name__
                                  ,template_folder='../templates'
                                  ,static_folder='../static')

"""##########系统管理功能组- 用户管理部分的url行为定义#############################################

"""
@userManagement.route('/userManagement/',methods=['GET'])
def getUserManagement():
    return render_template('userManagement.html')

@userManagement.route('/userManagement/tableList/',methods=['POST'])
def userManagement_userList():
    filter_str = ''
    for key in request.form:
        if len(request.form[key]) > 0:
            if len(filter_str) > 0:
                filter_str += ' and '
            filter_str += " " + key + "='" + request.form[key] + "'"

    with userManagement.open_resource("../static/table_schemas/userManagement.json") as json_file:
        users_schema = json.load(json_file)

    resp = commonFunction.load_alertMsg_session()
    # 读表内容
    try:
        users_data = query_user_join_identity(text(filter_str))
        identity_list = Identities.get_identity_list(Identities())

        opt_list ={}
        opt_list["identityName"] = identity_list

        select_dict = commonFunction.construct_select_dict(users_schema)
        table_res = {"succeed": True,
                "table_schema_list":users_schema,
                "table_data":users_data,
                "opt_list":opt_list,
                "select_dict":select_dict}
        resp.update(table_res)
    except Exception,e:
        resp = {
            "succeed":False,
            "alertType":"danger",
            "alertMsg":traceback.format_exc()
        }
    print str(resp)
    resp = json.dumps(resp)
    return resp

def query_user_join_identity(filter_str):
    users_data = db_session.query(Users.userid, Users.username, Identities.identityName, Users.email, Users.lastTaskId). \
        join(Identities, Identities.identity == Users.identity).filter(filter_str).distinct().all()

    for i in range(0, len(users_data)):
        users_data[i]  = {
            u"userid": int(users_data[i].userid),
            u"username": users_data[i].username,
            u"identityName": users_data[i].identityName,
            u"email": users_data[i].email,
            u"lastTaskId": users_data[i].lastTaskId
        }
    return users_data


"""#########################以下是”添加“有关的url行为及调用定义
为已有的功能组添加具体的功能，新功能不可以与同一功能组下的功能同名
"""
@userManagement.route('/userManagement/plus/',methods=['POST'])
def userManagement_plus():
    not_null_list = set(["userame", "identityName"])
    alertMsg = []
    plus_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    if check == True:
        check = check_plus_exist(plus_unit_dict, alertMsg)
        if check == True:
            check = insert_plus(plus_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp

def check_plus_exist(plus_unit_dict, alertMsg):
    ###
    to_plus_username = plus_unit_dict["username"]
    check_section = db_session.query(Users).\
        filter(Users.username == to_plus_username ).first()
    if check_section != None: ###存在同名元组
        alertMsg.append(u"已存在同名用户 " + to_plus_username + " ,添加失败!")
        return False
    return True

def insert_plus(plus_unit_dict, alertMsg):
    username = plus_unit_dict["username"]
    identityName = plus_unit_dict['identityName']
    email = plus_unit_dict['email']
    identity = Identities.query.filter(Identities.identityName == identityName).first().identity
    init_passwd = commonFunction.caculate_md5("123456")
    plus_unit = Users(passwd=init_passwd, username=username, identity=identity, email=email)
    try:
        db_session.add(plus_unit)
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True

"""#########################以下是”修改“有关的url行为及调用定义
为已有的功能组添加具体的功能，新功能不可以与同一功能组下的功能同名
"""
@userManagement.route('/userManagement/edit/',methods=['POST'])
def userManagement_edit():
    not_null_list = set(["userid"])
    alertMsg = []
    edit_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    if check == True:
        check = check_edit_exist(edit_unit_dict, alertMsg)
        if check == True:
            check = insert_edit(edit_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp

def check_edit_exist(edit_unit_dict, alertMsg):
    ###检查同名不同Id的用户
    to_edit_username = edit_unit_dict["username"]
    to_edit_userid = edit_unit_dict["userid"]
    check_section = db_session.query(Users).\
        filter(Users.username == to_edit_username , Users.userid != to_edit_userid).first()
    if check_section != None: ###存在同名元组
        alertMsg.append(u"已存在同名用户 " + to_edit_username + " ,修改失败!")
        return False
    return True

def insert_edit(edit_unit_dict, alertMsg):
    ###此处的修改不涉及密码
    to_edit_userid = edit_unit_dict["userid"]
    username = edit_unit_dict["username"]
    identityName = edit_unit_dict['identityName']
    email = edit_unit_dict['email']
    identity = Identities.query.filter(Identities.identityName == identityName).first().identity
    try:
        db_session.query(Users).filter(Users.userid == to_edit_userid).\
            update({
            Users.username: username,
            Users.identity: identity,
            Users.email:email
        })
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True

"""#########################以下是”删除“有关的url行为及调用定义
为已有的功能组添加具体的功能，新功能不可以与同一功能组下的功能同名
"""
@userManagement.route('/userManagement/delete/',methods=['POST'])
def userManagement_delete():
    not_null_list = set(["userid"])
    alertMsg = []

    delete_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    check = delete_row(delete_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp

def delete_row(delete_unit_dict, alertMsg):
    ###如果有userid就删用户
    userid = delete_unit_dict['userid']
    try:
        db_session.query(Users).filter(Users.userid == int(userid)).delete()
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True
