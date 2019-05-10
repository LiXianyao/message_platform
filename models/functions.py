# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class Functions(Base):

    #表名
    __tablename__ ='function'
    #表结构
    functionId = Column(Integer, autoincrement=True, primary_key=True)
    functionName = Column(String(32),nullable=False)
    functionSrc = Column(String(32), nullable=False)
    sectionId = Column(Integer, ForeignKey('functionSection.sectionId',ondelete='CASCADE',onupdate='CASCADE'))
    #关联变量名 = relationship('关联表名'，lazy='dynamic'不级联增加，ForeignKey('table.column'))

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, functionName=None, functionSrc=None,sectionId=None, utility=None, from_result=False):
         if from_result == True:
            self.functionId = utility.functionId
            self.functionName = utility.functionName
            self.functionSrc = utility.functionSrc
            self.sectionId = utility.sectionId
         else:
            self.functionName = functionName
            self.functionSrc = functionSrc
            self.sectionId = sectionId

    def __repr__(self):
        function_dict = {
            u"functionId":int(self.functionId),
            u"functionName":self.functionName,
            u"functionSrc":self.functionSrc,
            u"sectionId":self.sectionId
        }
        return str(function_dict)

    def __dir__(self):
        function_dict = {
            u"functionId":int(self.functionId),
            u"functionName":self.functionName,
            u"functionSrc":self.functionSrc,
            u"sectionId":self.sectionId
        }
        return function_dict

    def get_function_list(self):
        function_data = db_session.query(Functions.functionId, Functions.functionName).distinct().all()
        function_list = []
        for i in range(0, len(function_data)):
            function_list.append({"id": int(function_data[i].functionId), "name": function_data[i].functionName})
        return function_list


