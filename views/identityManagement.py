# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
import json
import commonFunction
from models.functions import Functions
from models.identities import Identities
from database import db_session
from sqlalchemy import text
import traceback

identityManagement = Blueprint('identityManagement'
                                  ,__name__
                                  ,template_folder='../templates'
                                  ,static_folder='../static')

"""##########系统管理功能组- 用户管理部分的url行为定义#############################################

"""
@identityManagement.route('/identityManagement/',methods=['GET'])
def getidentityManagement():
    return render_template('identityManagement.html')

@identityManagement.route('/identityManagement/tableList/',methods=['POST'])
def identityManagement_identityList():
    filter_str = ''
    for key in request.form:
        if len(request.form[key]) > 0:
            if len(filter_str) > 0:
                filter_str += ' and '
            filter_str += " " + key + "='" + request.form[key] + "'"

    with identityManagement.open_resource("../static/table_schemas/identityManagement.json") as json_file:
        identities_schema = json.load(json_file)

    resp = commonFunction.load_alertMsg_session()
    # 读表内容
    try:
        select_dict = commonFunction.construct_select_dict(identities_schema)
        # 读表内容
        identities_data = query_identity_join_function(text(filter_str))
        function_list = Functions.get_function_list(Functions())
        identity_list = Identities.get_identity_list(Identities())

        opt_list ={}
        opt_list["identityName"] = identity_list
        opt_list["functionName"] = function_list

        table_res= {"succeed": True, "table_schema_list":identities_schema,
                "table_data":identities_data,
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

def query_identity_join_function(filter_str):
    identities_data = db_session.query(Identities.id,Identities.identity, Identities.identityName,  Functions.functionName). \
        join(Functions, Identities.authority == Functions.functionId).filter(filter_str).order_by(Identities.identity.asc()).distinct().all()

    for i in range(0, len(identities_data)):
        identities_data[i]  = {
            u"id": int(identities_data[i].id),
            u"identity": int(identities_data[i].identity),
            u"identityName": identities_data[i].identityName,
            u"functionName": identities_data[i].functionName
        }
    return identities_data

"""#########################以下是”新建“有关的url行为及调用定义
添加一个新的功能组，不可与原有功能组同名
"""
@identityManagement.route('/identityManagement/new/',methods=['POST'])
def identityManagement_new():
    not_null_list = set(["identityName","functionName"])
    alertMsg = []
    new_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    if check:
        check = check_new_exist(new_unit_dict, alertMsg)
        if check:
            check = insert_new(new_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp


def insert_new(new_unit_dict, alertMsg):
    ##插入一个新的角色
    identityName = new_unit_dict['identityName']
    functionName = new_unit_dict['functionName']
    ##新的identity 编号取一个表中没有的数
    identity = Identities.query.order_by(Identities.identity.desc()).first().identity + 1
    authority = Functions.query.filter(Functions.functionName == functionName).first().functionId
    new_unit = Identities(identityName=identityName, identity=identity, authority=authority)
    try:
        db_session.add(new_unit)
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True

def check_new_exist(new_unit_dict, alertMsg):
    ##检查是否有同名角色存在
    to_new = new_unit_dict["identityName"]
    check_section = db_session.query(Identities).\
        filter(Identities.identityName == to_new).first()
    if check_section != None: ###存在同名元组
        alertMsg.append(u"角色名 " + to_new + u" 已存在!")
        return False
    return True

"""#########################以下是”添加“有关的url行为及调用定义
为已有的角色添加具体的功能，新功能不可以与该角色已有的功能同名
"""
@identityManagement.route('/identityManagement/plus/',methods=['POST'])
def identityManagement_plus():
    not_null_list = set(["identity", "identityName", "functionName"])
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
    ###检查此角色是否已经有了同名的功能
    to_plus_identity = plus_unit_dict["identityName"]
    to_plus_func = plus_unit_dict["functionName"]
    check_section = db_session.query(Identities). \
        join(Functions, Identities.authority == Functions.functionId). \
        filter(Identities.identityName == to_plus_identity, Functions.functionName == to_plus_func).first()
    if check_section != None:  ###存在同名元组
        alertMsg.append(u"角色 " + to_plus_identity + u"中已存在功能 " + to_plus_func + " !")
        return False
    return True

def insert_plus(plus_unit_dict, alertMsg):
    ###为指定角色添加指定功能功能
    identityName = plus_unit_dict['identityName']
    functionName = plus_unit_dict['functionName']
    identity = Identities.query.filter(Identities.identityName == identityName).first().identity
    authority = Functions.query.filter(Functions.functionName == functionName).first().functionId
    plus_unit = Identities(identityName=identityName, identity=identity, authority=authority)
    try:
        db_session.add(plus_unit)
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True

"""#########################以下是”删除“有关的url行为及调用定义
为已有的功能组添加具体的功能，新功能不可以与同一功能组下的功能同名
"""
@identityManagement.route('/identityManagement/delete/',methods=['POST'])
def identityManagement_delete():
    not_null_list = set(["id"])
    alertMsg = []

    delete_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    check = delete_row(delete_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp

def delete_row(delete_unit_dict, alertMsg):
    ###删除一个角色的功能
    identity_id = delete_unit_dict['id']
    try:
        db_session.query(Identities).filter(Identities.id == int(identity_id)).delete()
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True
