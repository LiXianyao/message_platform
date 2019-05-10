# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
import json
import commonFunction
from models.templatesTaskContent import templatesTaskContent
from models.identities import Identities
from database import db_session
from sqlalchemy import text
import traceback

templateTaskContent = Blueprint('templateTaskContent'
                                  ,__name__
                                  ,template_folder='../templates'
                                  ,static_folder='../static')

"""##########系统管理功能组- 用户管理部分的url行为定义#############################################

"""
@templateTaskContent.route('/templateTaskContent/',methods=['GET'])
def gettemplateTaskContent():
    return render_template('templateTaskContent.html')

@templateTaskContent.route('/templateTaskContent/tableList/',methods=['POST'])
def templateTaskContent_tableList():
    filter_str = ''
    target_table = ''
    for key in request.form:
        if key == 'target_table':
            target_table = request.form[key]
            continue
        if len(request.form[key]) > 0:
            if len(filter_str) > 0:
                filter_str += ' and '
            filter_str += " " + key + "='" + request.form[key] + "'"

    with templateTaskContent.open_resource("../static/table_schemas/templateTaskContent.json") as json_file:
        table_schema = json.load(json_file)

    resp = commonFunction.load_alertMsg_session()
    # 读表内容
    try:
        ###确定可以展示的数据表
        templateTask_list = [{"id":1,"name":"msgContents_test9"}]

        if len(target_table) == 0:##没有指定目标表
            target_data = []
        else:  ##去查那个指定表，用上filter
            target_data = query_templateTaskContent(target_table, filter_str)
            pass

        opt_list ={}
        opt_list["templateTask"] = templateTask_list

        select_dict = commonFunction.construct_select_dict(table_schema)
        table_res = {"succeed": True,
                "table_schema_list":table_schema,
                "table_data":target_data,
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

def query_templateTaskContent(target_table, filter_str):
    toShow = templatesTaskContent(target_table)
    target_data = toShow.query.filter(filter_str).all()
    
    for i in range(0, len(target_data)):
        target_data[i]  = {
            u"id": int(target_data[i].id),
            u"content": target_data[i].content,
            u"templateid": target_data[i].templateid,
            u"newTpl": target_data[i].newTpl,
        }
    return target_data
