# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request,session
import json
import commonFunction
from models.functions import Functions
from models.sections import Sections
from database import db_session
from sqlalchemy import text
import traceback

functionManagement = Blueprint('functionManagement'
                                  ,__name__
                                  ,template_folder='../templates'
                                  ,static_folder='../static')

"""##########系统管理功能组- 用户管理部分的url行为定义#############################################

"""



@functionManagement.route('/functionManagement/',methods=['GET'])
def getfunctionManagement():
    return render_template('functionManagement.html')

@functionManagement.route('/functionManagement/tableList/',methods=['POST'])
def functionManagement_functionList():
    filter_str = ''
    for key in request.form:
        if len(request.form[key]) > 0:
            if len(filter_str) > 0:
                filter_str += ' and '
            filter_str += " " + key + "='" + request.form[key] + "'"

    with functionManagement.open_resource("../static/table_schemas/functionManagement.json") as json_file:
        functions_schema = json.load(json_file)

    resp = commonFunction.load_alertMsg_session()
    # 读表内容
    try:
        functions_data = query_section_join_function(text(filter_str))
        function_list = Functions.get_function_list(Functions())
        section_list = Sections.get_section_list(Sections())

        opt_list ={}
        opt_list["functionName"] = function_list
        opt_list["sectionName"] = section_list

        select_dict = commonFunction.construct_select_dict(functions_schema)
        table_res = {"succeed": True,
                "table_schema_list":functions_schema,
                "table_data":functions_data,
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

def query_section_join_function(filter_str):
    functions_data = db_session.query(Sections.sectionId, Sections.sectionName,Functions.functionId, Functions.functionName, Functions.functionSrc). \
        join(Functions, Sections.sectionId == Functions.sectionId ,isouter=True).filter(filter_str).order_by(Sections.sectionId.asc()).all()

    for i in range(0, len(functions_data)):
        if functions_data[i].functionId == None:
            functions_data[i] = {
                u"sectionId": int(functions_data[i].sectionId),
                u"sectionName": functions_data[i].sectionName,
            }
        else:
            functions_data[i]  = {
                u"functionId":int(functions_data[i].functionId),
                u"sectionId": int(functions_data[i].sectionId),
                u"sectionName": functions_data[i].sectionName,
                u"functionSrc": functions_data[i].functionSrc,
                u"functionName": functions_data[i].functionName
            }
    return functions_data

"""#########################以下是”新建“有关的url行为及调用定义
添加一个新的功能组，不可与原有功能组同名
"""
@functionManagement.route('/functionManagement/new/',methods=['POST'])
def functionManagement_new():
    not_null_list = set(["sectionName"])
    alertMsg = []
    new_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    if check == True:
        check = check_new_exist(new_unit_dict, alertMsg)
        if check == True:
            check = insert_new(new_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp

def insert_new(new_unit_dict, alertMsg):
    new_unit = Sections(sectionName=new_unit_dict["sectionName"])
    try:
        db_session.add(new_unit)
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True

def check_new_exist(new_unit_dict, alertMsg):
    to_new = new_unit_dict["sectionName"]
    check_section = db_session.query(Sections).\
        filter("sectionName='" + to_new + "'").first()
    if check_section != None: ###存在同名元组
        alertMsg.append(u"功能组 " + to_new + u" 已存在!")
        return False
    return True

"""#########################以下是”添加“有关的url行为及调用定义
为已有的功能组添加具体的功能，新功能不可以与同一功能组下的功能同名
"""
@functionManagement.route('/functionManagement/plus/',methods=['POST'])
def functionManagement_plus():
    not_null_list = set(["sectionName", "functionName", "functionSrc"])
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
    to_plus_group = plus_unit_dict["sectionName"]
    to_plus_func = plus_unit_dict["functionName"]
    check_section = db_session.query(Functions).\
        join(Sections,Sections.sectionId == Functions.sectionId).\
        filter(Sections.sectionName == to_plus_group, Functions.functionName == to_plus_func).first()
    if check_section != None: ###存在同名元组
        alertMsg.append(u"功能组 " + to_plus_group + u"中已存在功能 " + to_plus_func + " !")
        return False
    return True

def insert_plus(plus_unit_dict, alertMsg):
    to_plus_group = plus_unit_dict["sectionName"]
    functionName = plus_unit_dict['functionName']
    functionSrc = plus_unit_dict['functionSrc']
    sectionId = Sections.query.filter("sectionName='" + to_plus_group + "'").first().sectionId
    plus_unit = Functions(functionName=functionName, functionSrc=functionSrc, sectionId=sectionId)
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
@functionManagement.route('/functionManagement/edit/',methods=['POST'])
def functionManagement_edit():
    not_null_list = set(["sectionName", "functionName", "functionSrc", "functionId"])
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
    to_edit_group = edit_unit_dict["sectionName"]
    to_edit_func = edit_unit_dict["functionName"]
    to_edit_func_id = edit_unit_dict["functionId"]
    if(to_edit_func_id == u"undefined"):
        alertMsg.append(u"功能组" + to_edit_group + u"尚未定义功能，请通过 '添加功能' 为其添加")
        return False
    check_section = db_session.query(Functions).\
        join(Sections,Sections.sectionId == Functions.sectionId).\
        filter(Sections.sectionName == to_edit_group,
               Functions.functionName == to_edit_func,
               Functions.functionId != to_edit_func_id).first()
    if check_section != None: ###存在同名元组
        alertMsg.append(u"功能组 " + to_edit_group + u"中已存在功能 " + to_edit_func + " !")
        return False
    return True

def insert_edit(edit_unit_dict, alertMsg):
    to_edit_group = edit_unit_dict["sectionName"]
    functionName = edit_unit_dict['functionName']
    functionSrc = edit_unit_dict['functionSrc']
    functionId = int(edit_unit_dict['functionId'])
    sectionId = Sections.query.filter("sectionName='" + to_edit_group + "'").first().sectionId
    try:
        db_session.query(Functions).filter(Functions.functionId == functionId).\
            update({Functions.functionName: functionName,
                 Functions.functionSrc: functionSrc,
                 Functions.sectionId : sectionId})
        db_session.commit()
    except:
        alertMsg.append(traceback.format_exc())
        return False
    return True

"""#########################以下是”删除“有关的url行为及调用定义
为已有的功能组添加具体的功能，新功能不可以与同一功能组下的功能同名
"""
@functionManagement.route('/functionManagement/delete/',methods=['POST'])
def functionManagement_delete():
    not_null_list = set(["functionId"])
    alertMsg = []

    delete_unit_dict, check = commonFunction.form2dict(request=request, not_null_list=not_null_list, alertMsg=alertMsg)

    check = delete_row(delete_unit_dict, alertMsg)

    resp = commonFunction.form_alert_resp(check, alertMsg)
    commonFunction.save_alertMsg_session(resp['alertType'], resp['alertMsg'])
    print str(resp)
    resp = json.dumps(resp)
    return resp

def delete_row(delete_unit_dict, alertMsg):
    ###如果有functionId就删功能，否则删功能组
    functionId = delete_unit_dict['functionId']
    if (functionId != u"undefined"):
        try:
            db_session.query(Functions).filter(Functions.functionId == int(functionId)).delete()
            db_session.commit()
        except:
            alertMsg.append(traceback.format_exc())
            return False
    else:
        sectionId = delete_unit_dict['sectionId']
        try:
            db_session.query(Sections).filter(Sections.sectionId == int(sectionId)).delete()
            db_session.commit()
        except:
            alertMsg.append(traceback.format_exc())
            return False
    return True