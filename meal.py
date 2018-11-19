#!/usr/bin/python
#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
class Meal(Base):
    __tablename__ = 'meal'

    meal_id = Column(Integer, primary_key = True)
    date_id = Column(Integer, primary_key = True)
    canteen_id = Column(Integer, primary_key = True)
    name = Column(String)
    price0 = Column(String)
    price1 = Column(String)

    def __init__(self, canteen_id, date_id, meal_id, name, price0, price1):
        self.meal_id = meal_id
        self.date_id = date_id
        self.canteen_id = canteen_id
        self.name = name
        self.price0 = price0
        self.price1 = price1

    def __repr__(self):
        return "<Meal(%d, %d, %d, %s, %s, %s)>" % (self.canteen_id,
                                                   self.date_id,
                                                   self.meal_id,
                                                   self.name,
                                                   self.price0,
                                                   self.price1)

    def save(self, db):
        result = db.session.query(Meal).filter_by(meal_id=self.meal_id,
                                                  date_id=self.date_id,
                                                  canteen_id=self.canteen_id).first()
        if result:
            result.name = self.name
            result.price0 = self.price0
            result.price1 = self.price1
        else:
            db.session.add(self)
        db.session.commit()
