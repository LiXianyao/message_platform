# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey, Boolean, TIMESTAMP
from database import Base,db_session
class RedisServer(Base):

    #表名
    __tablename__ ='redisServer'
    #表结构
    severId = Column(Integer, autoincrement=True, primary_key=True)
    serverIp = Column(String(16), nullable=False)
    createdBy = Column(String(64), nullable=False)
    dbId = Column(Integer, nullable=False)
    isDefault = Column(Boolean, nullable=False)
    createdTime = Column(TIMESTAMP(True), nullable=False)

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, serverId, serverIp, serverPort, dbId, isDefault, createdBy):
        self.serverId = serverId
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.dbId = dbId
        self.isDefault = isDefault
        self.createdBy = createdBy

    def __repr__(self):
        server_dict = {
            u"serverId": int(self.serverId),
            u"serverIp": self.serverIp,
            u"serverPort": self.serverPort,
            u"dbId": int(self.dbId)
        }
        return str(server_dict)

    def __dir__(self):
        server_dict = {
            u"serverId": int(self.serverId),
            u"serverIp": self.serverIp,
            u"serverPort": self.serverPort,
            u"dbId": int(self.dbId)
        }
        return server_dict


