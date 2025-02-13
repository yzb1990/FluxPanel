# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from config.database import BaseMixin, Base


class SysTable(Base, BaseMixin):
    __tablename__ = "sys_table"

    align = Column(String(255), nullable=False, default='left', comment='对其方式')

    field_name = Column(String(255), nullable=False, comment='字段名')

    fixed = Column(String(1), nullable=False, default='0', comment='固定表头')

    label = Column(String(255), nullable=False, comment='字段标签')

    label_tip = Column(String(255), comment='字段标签解释')

    prop = Column(String(255), nullable=False, comment='驼峰属性')

    show = Column(String(1), nullable=False, default='1', comment='可见')

    sortable = Column(String(1), nullable=False, default='0', comment='可排序')

    table_name = Column(String(255), nullable=False, comment='表名')

    tooltip = Column(String(1), nullable=False, default='1', comment='超出隐藏')

    update_by = Column(Integer, comment='更新者')

    update_by_name = Column(String(255), comment='更新者')

    width = Column(Integer, nullable=False, default=150, comment='宽度')

    sequence = Column(Integer, nullable=False, default=0, comment='字段顺序')

