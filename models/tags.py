# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class Tags(Base):

    #表名
    __tablename__ ='tag'
    #表结构
    tagCode = Column(String(8), primary_key=True)
    tagName = Column(String(32),nullable=False)
    tagType = Column(String(16),nullable=False)

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, tagCode, tagType=None, tagName=None):
        self.tagCode = tagCode
        self.tagName = tagName
        self.tagType = tagType

    def __repr__(self):
        tag_dict = {
            u"tagCode":self.tagCode,
            u"tagName":self.tagName,
            u"tagType":self.tagType
        }
        return str(tag_dict)

    def __dir__(self):
        tag_dict = {
            u"tagCode": self.tagCode,
            u"tagName": self.tagName,
            u"tagType":self.tagType
        }
        return tag_dict

