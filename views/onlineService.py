# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
import json
import commonFunction
import requests
import traceback

onlineService = Blueprint('onlineService'
                                  ,__name__
                                  ,template_folder='../templates'
                                  ,static_folder='../static')

"""##########系统管理功能组- 用户管理部分的url行为定义#############################################

"""
@onlineService.route('/onlineService/',methods=['GET'])
def getonlineService():
    return render_template('onlineService.html')

@onlineService.route('/onlineService/OfflineRiskClassification/',methods=['POST'])
@onlineService.route('/onlineService/IndustryClassification/',methods=['POST'])
@onlineService.route('/onlineService/TemplateMatching/',methods=['POST'])
def onlineService_offlineRiskClassification():
    #print "json == ", request.json

    resp = {}
    res_seg = {"OfflineRiskClassification": ["offlineRisk", "offlineRiskProb"],
               "IndustryClassification": ["industry1", "industry1Prob", "industry2", "industry2Prob", "industry3",
                                          "industry3Prob"],
               "TemplateMatching": ["tcode", "template"]}
    request_url = {"OfflineRiskClassification": "offlineRiskClassification",
                   "IndustryClassification": "industryClassification",
                   "TemplateMatching": "templateMatching"}
    try:
        target = request.json["target"]
        r = requests.post("http://10.109.246.100:5001/" + request_url[target], json=request.json)
        return_msg = json.loads(r.text)
        if return_msg['resultCode'] == '0':
            return_msg.update({"succeed": False,
                               "alertType": "danger",
                                "alertMsg": return_msg["message"]})
        else:
            return_msg.update( {"succeed": True, "displayList":res_seg[target]})
        resp.update(return_msg)
        print str(resp).replace('u\'', '\'').decode("unicode-escape")
    except Exception,e:
        resp = {
            "succeed":False,
            "alertType":"danger",
            "alertMsg":traceback.format_exc()
        }
    print str(resp)
    resp = json.dumps(resp)
    return resp