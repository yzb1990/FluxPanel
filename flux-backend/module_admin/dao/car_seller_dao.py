# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.car_seller_do import CarSeller
from module_admin.entity.vo.car_seller_vo import CarSellerPageModel, CarSellerModel
from utils.page_util import PageUtil, PageResponseModel


class CarSellerDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, car_seller_id: int) -> CarSeller:
        """根据主键获取单条记录"""
        car_seller = (((await db.execute(
                            select(CarSeller)
                            .where(CarSeller.id == car_seller_id)))
                       .scalars())
                       .first())
        return car_seller

    """
    查询
    """
    @classmethod
    async def get_car_seller_list(cls, db: AsyncSession,
                             query_object: CarSellerPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(CarSeller)
            .where(
                CarSeller.age == query_object.age if query_object.age else True,
                CarSeller.car_type == query_object.car_type if query_object.car_type else True,
                CarSeller.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(CarSeller.create_time))
            .distinct()
        )
        car_seller_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return car_seller_list


    @classmethod
    async def add_car_seller(cls, db: AsyncSession, add_model: CarSellerModel, auto_commit: bool = True) -> CarSeller:
        """
        增加
        """
        car_seller =  CarSeller(**add_model.model_dump(exclude_unset=True))
        db.add(car_seller)
        await db.flush()
        if auto_commit:
            await db.commit()
        return car_seller

    @classmethod
    async def edit_car_seller(cls, db: AsyncSession, edit_model: CarSellerModel, auto_commit: bool = True) -> CarSeller:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(CarSeller), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_car_seller(cls, db: AsyncSession, car_seller_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(CarSeller).where(CarSeller.id.in_(car_seller_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(CarSeller).where(CarSeller.id.in_(car_seller_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()