#!/usr/bin/python
#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DB:
    def __init__(self):
        self.engine = create_engine("mysql+mysqldb://studentenwerk:studentenwerk_pwd@localhost/studentenwerk")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save(self, cls, inst):
        result = self.session.query(cls).filter_by(inst).all()
        if result:
            print(result)
        else:
            self.session.add(inst)
        self.session.commit()
