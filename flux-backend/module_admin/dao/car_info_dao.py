# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.car_info_do import CarInfo
from module_admin.entity.vo.car_info_vo import CarInfoPageModel, CarInfoModel
from utils.page_util import PageUtil, PageResponseModel


class CarInfoDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, car_info_id: int) -> CarInfo:
        """根据主键获取单条记录"""
        car_info = (((await db.execute(
                            select(CarInfo)
                            .where(CarInfo.id == car_info_id)))
                       .scalars())
                       .first())
        return car_info

    """
    查询
    """
    @classmethod
    async def get_car_info_list(cls, db: AsyncSession,
                             query_object: CarInfoPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(CarInfo)
            .where(
                CarInfo.car_name.like(f"%{query_object.car_name}%") if query_object.car_name else True,
                CarInfo.car_type == query_object.car_type if query_object.car_type else True,
                CarInfo.create_time.between(query_object.begin_create_time, query_object.end_create_time) if query_object.create_time else True,
                CarInfo.lng.like(f"%{query_object.lng}%") if query_object.lng else True,
                CarInfo.location.like(f"%{query_object.location}%") if query_object.location else True,
                CarInfo.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(CarInfo.create_time))
            .distinct()
        )
        car_info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return car_info_list


    @classmethod
    async def add_car_info(cls, db: AsyncSession, add_model: CarInfoModel, auto_commit: bool = True) -> CarInfo:
        """
        增加
        """
        car_info =  CarInfo(**add_model.model_dump(exclude_unset=True))
        db.add(car_info)
        await db.flush()
        if auto_commit:
            await db.commit()
        return car_info

    @classmethod
    async def edit_car_info(cls, db: AsyncSession, edit_model: CarInfoModel, auto_commit: bool = True) -> CarInfo:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(CarInfo), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_car_info(cls, db: AsyncSession, car_info_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(CarInfo).where(CarInfo.id.in_(car_info_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(CarInfo).where(CarInfo.id.in_(car_info_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()