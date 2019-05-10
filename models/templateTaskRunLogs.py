# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class TemplateTaskokcnts(Base):

    #表名
    __tablename__ ='templateTaskokcnt'
    #表结构
    taskid = Column(String(16), ForeignKey('templateTask.taskid', ondelete='NO ACTION', onupdate='CASCADE'),  nullable=False, primary_key=True)
    status = Column(String(32), nullable=False)
    lastUpdateTime = Column(String(16), nullable=False)
    analysisStartTime = Column(String(16), nullable=True)
    analysisEndTime = Column(String(16), nullable=True)
    total = Column(Integer, nullable=True)
    okcnt = Column(Integer, nullable=True)
    tcnt = Column(Integer, nullable=True)
    invalidcnt = Column(Integer, nullable=True)
    misscnt = Column(Integer, nullable=True)
    matchcnt = Column(Integer, nullable=True)
    newTplCnt = Column(Integer, nullable=True)


    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, taskid=None, total=None, status=None, lastUpdateTime=None, analysisStartTime=None, okcnt=None,
                 templateServer=None, dataServer=None, analysisEndTime=None):

        self.taskid = taskid
        self.total = total
        self.status = status
        self.lastUpdateTime = lastUpdateTime
        self.analysisStartTime = analysisStartTime
        self.okcnt = okcnt
        self.tcnt = templateServer
        self.dataServer = dataServer
        self.analysisEndTime = analysisEndTime

    def __repr__(self):
        templatetask_dict = {
            u"taskid": self.taskid,
            u"total": self.total,
            u"status": self.status,
            u"analysisStartTime": self.analysisStartTime,
            u"okcnt": int(self.okcnt),
        }
        return str(templatetask_dict)

    def __dir__(self):
        templatetask_dict = {
            u"taskid": self.taskid,
            u"total": self.total,
            u"status": self.status,
            u"analysisStartTime": self.analysisStartTime,
            u"okcnt": int(self.okcnt),
        }
        return templatetask_dict


