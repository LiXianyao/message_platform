# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
import json
import commonFunction
from models.analysisTaskRes import analysisRes
from models.identities import Identities
from database import db_session, Base
from sqlalchemy import text
import traceback

analysisTasks = {}
analysisTaskRes = Blueprint('analysisTaskRes'
                                  ,__name__
                                  ,template_folder='../templates'
                                  ,static_folder='../static')

"""##########系统管理功能组- 用户管理部分的url行为定义#############################################

"""
@analysisTaskRes.route('/analysisTaskRes/',methods=['GET'])
def getanalysisTaskRes():
    return render_template('analysisTaskRes.html')

@analysisTaskRes.route('/analysisTaskRes/tableList/',methods=['POST'])
def analysisTaskRes_tableList():
    filter_str = ''
    target_table = ''
    offset = 0
    limit = 10
    for key in request.form:
        if key == 'task_id':
            target_table = request.form[key]
        elif key == 'offset':
            offset = request.form[key]
        elif key == 'limit':
            limit = request.form[key]
        if len(request.form[key]) > 0:
            if len(filter_str) > 0:
                filter_str += ' and '
            filter_str += " " + key + "='" + request.form[key] + "'"

    with analysisTaskRes.open_resource("../static/table_schemas/analysisTaskRes.json") as json_file:
        table_schema = json.load(json_file)

    resp = commonFunction.load_alertMsg_session()
    # 读表内容
    try:
        ###确定可以展示的数据表
        analysisTask_list = analysisRes.get_analysisRes_list(analysisRes(''))

        if len(target_table) == 0:##没有指定目标表
            target_data = []
        else:  ##去查那个指定表，用上filter
            target_data = query_analysisTaskRes(target_table, filter_str, offset, limit)
            pass

        opt_list ={}
        opt_list["task_id"] = analysisTask_list

        select_dict = commonFunction.construct_select_dict(table_schema)

        table_res = {"succeed": True,
                "table_schema_list":table_schema,
                "table_data":target_data,
                "opt_list":opt_list,
                "select_dict":select_dict,
                "now_page":0}
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

def query_analysisTaskRes(target_table, filter_str, offset=0, limit=100):
    try:
        toShow = analysisTasks[target_table]
    except:
        class analysisResTable(analysisRes, Base):
            __tablename__ = analysisRes.__tablename__ + target_table
        toShow = analysisResTable()
        analysisTasks[target_table] = toShow

    target_data = toShow.query.filter(text(filter_str)).order_by("sms_id").offset(offset).limit(limit).all()

    for i in range(0, len(target_data)):
        print target_data[i]
        target_data[i]  = {
            u"sms_id": int(target_data[i].sms_id),
            u"content": target_data[i].content,
            u"task_id": target_data[i].task_id,
            u"sign": target_data[i].sign,
            u"industry1": target_data[i].industry1,
            u"industry1_name": target_data[i].industry1_name,
            u"industry1_prob": round(float(target_data[i].industry1_prob),2),
            u"industry2": target_data[i].industry2,
            u"industry2_name": target_data[i].industry2_name,
            u"industry2_prob": round(float(target_data[i].industry2_prob),2),
            u"industry3": target_data[i].industry3,
            u"industry3_name": target_data[i].industry3_name,
            u"industry3_prob": round(float(target_data[i].industry3_prob),2),
            u"offline_risk": target_data[i].offline_risk,
            u"offline_risk_name": target_data[i].offline_risk_name,
            u"offline_risk_prob": round(float(target_data[i].offline_risk_prob),2),
            u"confidence": round(float(target_data[i].confidence),2)
        }
    return target_data[5:]
