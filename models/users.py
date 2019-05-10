# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class Users(Base):

    #表名
    __tablename__ ='user'
    #表结构
    userid = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String(64),nullable=False)
    passwd = Column(String(64),nullable=False)
    identity = Column(Integer, nullable=False)
    email =  Column(String(64),nullable=True)
    lastTaskId =  Column(String(16),nullable=True)
    #关联变量名 = relationship('关联表名'，lazy='dynamic'不级联增加，ForeignKey('table.column'))

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, passwd=None, username=None, identity=None, email=None, lastTaskId=None, utility=None, from_result=False):
         if from_result == True:
            self.userid = utility.userid
            self.username = utility.username
            self.identity = utility.identityname
            self.email = utility.email
            self.lastTaskId = utility.lastTaskId
         else:
            self.passwd = passwd
            self.username = username
            self.identity = identity
            self.email = email
            self.lastTaskId = lastTaskId

    def __repr__(self):
        user_dict = {
            u"userid":int(self.userid),
            u"username":self.username,
            u"identity":self.identity,
            u"email":self.email,
            u"lastTaskId":self.lastTaskId
        }
        return str(user_dict)

    def __dir__(self):
        user_dict = {
            u"userid": int(self.userid),
            u"username": self.username,
            u"identity": self.identity,
            u"email": self.email,
            u"lastTaskId": self.lastTaskId
        }
        return user_dict

