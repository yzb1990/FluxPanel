# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float, Numeric
from config.database import BaseMixin, Base


class CarInfo(Base, BaseMixin):
    __tablename__ = "car_info"

    car_name = Column(String, nullable=False, comment='小车名称')

    car_type = Column(Integer, nullable=False, comment='车辆类型')

    image = Column(String, comment='图片')

    lat = Column(Float, comment='纬度')

    lng = Column(Float, comment='经度')

    location = Column(String, nullable=False, comment='所在位置')

    manager = Column(Integer, comment='管理员ID')

    price = Column(Numeric, comment='价格')

