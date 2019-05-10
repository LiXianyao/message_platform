# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey
from database import Base,db_session
class Identities(Base):

    #表名
    __tablename__ ='identity'
    #表结构
    id = Column(Integer, autoincrement=True, primary_key=True)
    identity = Column(Integer,nullable=False)
    identityName = Column(String(32),nullable=False)
    authority = Column(Integer, ForeignKey('function.functionId', ondelete='CASCADE', onupdate='CASCADE'))
    #关联变量名 = relationship('关联表名'，lazy='dynamic'不级联增加，ForeignKey('table.column'))

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, identity=None, identityName=None, authority=None):
        self.identity = identity
        self.identityName = identityName
        self.authority = authority

    def __repr__(self):
        identity_dict = {
            u"identity":int(self.identity),
            u"identityName":self.identityName,
            u"authority":int(self.identity),
        }
        return str(identity_dict)

    def __dir__(self):
        identity_dict = {
            u"identity": int(self.identity),
            u"identityName": self.identityName,
            u"authority": int(self.authority),
        }
        return identity_dict

    def get_identity_list(self):
        identity_data = db_session.query(Identities.identity, Identities.identityName).distinct().all()
        identity_list = []
        for i in range(0, len(identity_data)):
            identity_list.append({"id": int(identity_data[i].identity), "name": identity_data[i].identityName})
        return identity_list
