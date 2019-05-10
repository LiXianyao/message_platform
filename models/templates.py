# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer
from database import Base,db_session
class Templates(Base):

    #表名
    __tablename__ ='templates'
    #表结构
    templateid = Column(String(16),  nullable=False, primary_key=True)
    sign = Column(String(256), nullable=False)
    content = Column(String(1024), nullable=False)
    smsCount = Column(Integer, nullable=False, default=0)
    tagStatus = Column(String(8), nullable=False, default='未标记')
    sample = Column(String(1024), nullable=False, default='')

    industry1 = Column(String(16), nullable=False, default='0')
    industry1Name = Column(String(16), nullable=False, default='0')
    industry2 = Column(String(16), nullable=False, default='0')
    industry2Name = Column(String(16), nullable=False, default='0')
    industry3 = Column(String(16), nullable=False, default='0')
    industry3Name = Column(String(16), nullable=False, default='0')
    offlineRisk = Column(String(16), nullable=False, default='0')
    offlineRiskName = Column(String(16), nullable=False, default='0')

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, templateid=None, sign=None, content=None, sample=None, smsCount=None, tagStatus=None):

        self.templateid = templateid
        self.sign = sign
        self.content = content
        self.sample = sample
        self.smsCount = smsCount
        self.tagStatus = tagStatus

    def __repr__(self):
        template_dict = {
            u"templateid": self.templateid,
            u"sign": self.sign,
            u"content": self.content,
            u"sample": self.sample,
            u"smsCount": int(self.smsCount),
        }
        return str(template_dict)

    def __dir__(self):
        template_dict = {
            u"templateid": self.templateid,
            u"sign": self.sign,
            u"content": self.content,
            u"sample": self.sample,
            u"smsCount": int(self.smsCount),
        }
        return template_dict


