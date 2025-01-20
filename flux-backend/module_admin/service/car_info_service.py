# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from module_admin.dao.car_info_dao import CarInfoDao
from module_admin.entity.do.car_info_do import CarInfo
from module_admin.entity.vo.car_info_vo import CarInfoPageModel, CarInfoModel


class CarInfoService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_car_info_list(cls, query_db: AsyncSession, query_object: CarInfoPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        car_info_list = await CarInfoDao.get_car_info_list(query_db, query_object, data_scope_sql, is_page=True)
        return car_info_list

    @classmethod
    async def get_car_info_by_id(cls, query_db: AsyncSession, car_info_id: int) -> CarInfoModel:
        car_info = await  CarInfoDao.get_by_id(query_db, car_info_id)
        car_info_model = CarInfoModel(**CamelCaseUtil.transform_result(car_info))
        return car_info_model


    @classmethod
    async def add_car_info(cls, query_db: AsyncSession, query_object: CarInfoModel) -> CarInfoModel:
        car_info = await CarInfoDao.add_car_info(query_db, query_object)
        car_info_model = CarInfoModel(**CamelCaseUtil.transform_result(car_info))
        return car_info_model


    @classmethod
    async def update_car_info(cls, query_db: AsyncSession, query_object: CarInfoModel) -> CarInfoModel:
        car_info = await CarInfoDao.edit_car_info(query_db, query_object)
        car_info_model = CarInfoModel(**CamelCaseUtil.transform_result(car_info))
        return car_info_model


    @classmethod
    async def del_car_info(cls, query_db: AsyncSession, car_info_ids: List[str]):
        await CarInfoDao.del_car_info(query_db, car_info_ids)


    @classmethod
    async def export_car_info_list(cls, query_db: AsyncSession, query_object: CarInfoPageModel, data_scope_sql) -> bytes:
        car_info_list = await CarInfoDao.get_car_info_list(query_db, query_object, data_scope_sql, is_page=False)
        mapping_dict = {
            'carName': '小车名称 ',
            'carType': '车辆类型 ',
            'createTime': '创建时间 ',
            'image': '图片 ',
            'lat': '纬度 ',
            'lng': '经度 ',
            'location': '所在位置 ',
            'manager': '管理员ID ',
            'price': '价格 ',
        }
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in car_info_list
        ]
        binary_data = export_list2excel(new_data)
        return binary_data