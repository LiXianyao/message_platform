# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session


class templatesTaskContent(Base):
    # 表名
    __tablename__ = 'msgContents_'
    # 表结构
    id = Column(Integer, nullable=False, primary_key=True)
    templateid = Column(String(16), nullable=False)
    content = Column(String(1024), nullable=False)
    newTpl = Column(Integer, nullable=False)
    query = db_session.query_property()

    def __init__(self, taskid, templateid=None, id=None, content=None, newTpl=None):
        self.__tablename__ = 'msgContents_' + taskid
        self.templateid = templateid
        self.id = id
        self.content = content
        self.newTpl = newTpl

    def __repr__(self):
        unit_dict = {
            u"id":int(self.id),
            u"templateid":self.templateid,
            u"content":self.content,
            u"newTpl":self.newTpl
        }
        return str(unit_dict)

    def __dir__(self):
        unit_dict = {
            u"id": int(self.id),
            u"templateid": self.templateid,
            u"content": self.content,
            u"newTpl": self.newTpl
        }
        return unit_dict

