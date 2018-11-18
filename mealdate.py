#!/usr/bin/python
#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
class MealDate(Base):
    __tablename__ = 'date'

    date_id = Column(Integer, primary_key = True)
    canteen_id = Column(Integer, primary_key = True)
    text = Column(String)

    def __init__(self, canteen_id, date_id, text):
        self.date_id = date_id
        self.canteen_id = canteen_id
        self.text = text

    def __repr__(self):
        return "<MealDate(%d, %d, %s)>" % (self.date_id,
                                           self.canteen_id,
                                           self.text)

    def save(self, db):
        result = db.session.query(MealDate).filter_by(date_id=self.date_id, canteen_id=self.canteen_id).first()
        if result:
            result.text = self.text
        else:
            db.session.add(self)
        db.session.commit()
