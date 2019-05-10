# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class Sections(Base):

    #表名
    __tablename__ ='functionSection'
    #表结构
    sectionId = Column(Integer, autoincrement=True, primary_key=True)
    sectionName = Column(String(32),nullable=False)

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, sectionName=None, utility=None, from_result=False):
         if from_result == True:
            self.sectionId= utility.sectionId
            self.sectionName = utility.sectionName
         else:
            self.sectionName = sectionName

    def __repr__(self):
        section_dict = {
            u"sectionId":int(self.sectionId),
            u"sectionName":self.sectionName,
        }
        return str(section_dict)

    def __dir__(self):
        section_dict = {
            u"sectionId":int(self.sectionId),
            u"sectionName":self.sectionName,
        }
        return section_dict

    def get_section_list(self):
        section_data = db_session.query(Sections.sectionId, Sections.sectionName).distinct().all()
        section_list = []
        for i in range(0, len(section_data)):
            section_list.append({"id": int(section_data[i].sectionId), "name": section_data[i].sectionName})
        return section_list


