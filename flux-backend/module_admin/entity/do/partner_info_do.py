# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, DateTime, String, Text, Integer, Float, Numeric
from config.database import BaseMixin, Base


class PartnerInfo(Base, BaseMixin):
    __tablename__ = "partner_info"

    description = Column(Text, comment='资料介绍')

    image = Column(String(255), comment='图片')

    lat = Column(Float, comment='纬度')

    lng = Column(Float, comment='经度')

    location = Column(String(255), comment='所在位置')

    partner_name = Column(String(255), comment='合作方名称')

    price = Column(Numeric, comment='价格')

