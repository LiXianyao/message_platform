# -*- coding: utf-8 -*-
from flask import session
import traceback
import hashlib

""""#########计算字符串的MD5值
"""
def caculate_md5(passwd):
    md5_coding = hashlib.md5()
    md5_coding.update(passwd.encode(encoding="utf-8"))
    return md5_coding.hexdigest()

""""#########请求表单->python diction的转化(检查是否有不可为空的字段取空）
"""
def form2dict(request, not_null_list, alertMsg):
    unit_dict = {}
    check = True
    for key in request.form:
        if len(request.form[key]) == 0 and ( key in not_null_list):
            check = False
            alertMsg .append( key + "字段的取值不可为空!")
        unit_dict[key] = request.form[key]
    return unit_dict, check

def save_alertMsg_session(alertType, alertMsg):
    session['alertType'] = alertType
    session['alertMsg'] = alertMsg

def load_alertMsg_session():
    if session.has_key("alertType") == False:
        return {}
    resp = {
        "alertType": session['alertType'],
        "alertMsg": session['alertMsg']
    }
    session.pop('alertType',None)
    session.pop('alertMsg', None)
    return resp

def construct_select_dict(json_dict):
    select_dict = {}
    action_type = ["search", "plus", "edit", "new"]
    for unit in json_dict:
        for action in action_type:
            key = action + "Type"
            if unit.has_key(key) and unit[key] == 'select':
                opt_list_name = unit["data"]
                try:
                    select_dict[key].append(opt_list_name)
                except:
                    select_dict[key] = [opt_list_name]

    return select_dict

def form_alert_resp(check, alertMsg):
    resp = {}
    if check == True:
        resp = {
            "succeed":True,
            "alertType":"success",
            "alertMsg":"操作成功!"
        }
    else:
        resp = {
            "succeed": False,
            "alertType": "warning",
            "alertMsg": "\n".join(alertMsg)
        }
    return resp