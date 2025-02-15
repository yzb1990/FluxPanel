# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Numeric
from config.database import BaseMixin, Base


class CarSeller(Base, BaseMixin):
    __tablename__ = "car_seller"

    age = Column(Integer, nullable=False, comment='年龄')

    car_type = Column(Integer, nullable=False, comment='车辆类型')

    driver_years = Column(Integer, nullable=False, comment='驾龄')

    image = Column(String(255), comment='图片')

    location = Column(String(255), comment='所在位置')

    name = Column(String(255), nullable=False, comment='销售名字')

    price = Column(Numeric, nullable=False, comment='价格')

