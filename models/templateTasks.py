# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class TemplateTasks(Base):

    #表名
    __tablename__ ='templateTask'
    #表结构
    taskid = Column(String(16),  nullable=False, primary_key=True)
    userid = Column(Integer, nullable=False, primary_key=True)
    status = Column(String(16), nullable=False)
    dataFileName = Column(String(16), nullable=False)
    runLog = Column(Integer, nullable=False)
    templateServer = Column(Integer, ForeignKey('redisServer.serverId', ondelete='NO ACTION', onupdate='CASCADE'))
    dataServer = Column(Integer, ForeignKey('redisServer.serverId', ondelete='NO ACTION', onupdate='CASCADE'))
    tagStatus = Column(String(8), nullable=False)


    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, taskid=None, userid=None, status=None, dataFileName=None, runLog=None,
                 templateServer=None, dataServer=None, tagStatus=None):

        self.taskid = taskid
        self.userid = userid
        self.status = status
        self.dataFileName = dataFileName
        self.runLog = runLog
        self.templateServer = templateServer
        self.dataServer = dataServer
        self.tagStatus = tagStatus

    def __repr__(self):
        templatetask_dict = {
            u"taskid": self.taskid,
            u"userid": self.userid,
            u"status": self.status,
            u"dataFileName": self.dataFileName,
            u"runLog": int(self.runLog),
        }
        return str(templatetask_dict)

    def __dir__(self):
        templatetask_dict = {
            u"taskid": self.taskid,
            u"userid": self.userid,
            u"status": self.status,
            u"dataFileName": self.dataFileName,
            u"runLog": int(self.runLog),
        }
        return templatetask_dict


