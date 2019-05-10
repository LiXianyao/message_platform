# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, INTEGER
from database import Base,db_session
class Entries(Base):
    #查询构造器、、、
    query = db_session.query_property()
    #表名
    __tablename__ ='entries'
    #表结构
    id = Column(INTEGER,primary_key=True,autoincrement=True)
    title = Column(String(255),nullable=True)
    text = Column(String(255),nullable=True)
    #关联变量名 = relationship('关联表名'，lazy='dynamic'不级联增加，ForeignKey('table.column'))

    def __init__(self,title,text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Entries %d,%r,%r>' % (self.id, self.text,self.title)

