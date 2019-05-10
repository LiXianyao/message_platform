# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey, Float
from database import Base,db_session,ins


class analysisRes(object):
    # 表名
    __tablename__ = 'analysisRes_'
    # 表结构
    sms_id = Column(Integer, nullable=False, primary_key=True)
    task_id = Column(String(16), nullable=False)
    sign = Column(String(1024), nullable=False)
    content = Column(String(1024), nullable=False)
    industry1 = Column(String(16), nullable=True)
    industry1_name = Column(String(16), nullable=True)
    industry1_prob = Column(Float(8, 4), nullable=True)
    industry2 = Column(String(16), nullable=True)
    industry2_name = Column(String(16), nullable=True)
    industry2_prob = Column(Float(8, 4), nullable=True)
    industry3 = Column(String(16), nullable=True)
    industry3_name = Column(String(16), nullable=True)
    industry3_prob = Column(Float(8, 4), nullable=True)
    confidence = Column(Float(8, 4), nullable=True)
    offline_risk = Column(String(16), nullable=True)
    offline_risk_name = Column(String(16), nullable=True)
    offline_risk_prob = Column(Float(8, 4), nullable=True)

    def __init__(self, sms_id=None, task_id=None, content=None, sign=None):
        self.sms_id = sms_id
        self.task_id = task_id
        self.content = content
        self.sign = sign

    def __repr__(self):
        unit_dict = {
            u"task_id":self.task_id,
            u"sms_id":int(self.sms_id),
            u"content":self.content,
            u"sign":self.sign
        }
        return str(unit_dict)

    def __dir__(self):
        unit_dict = {
            u"task_id": self.task_id,
            u"sms_id": int(self.sms_id),
            u"content": self.content,
            u"sign": self.sign
        }
        return unit_dict

    def get_analysisRes_list(self):
        analysisRes_list = []
        listlen = 0
        for _t in ins.get_table_names():
            if _t.find(self.__tablename__) > -1:
                taskid = _t.split("_")[-1]
                analysisRes_list.append({"id": listlen, "name": taskid})
                listlen += 1
        print analysisRes_list
        return analysisRes_list


