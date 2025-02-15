# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from module_admin.dao.car_seller_dao import CarSellerDao
from module_admin.entity.do.car_seller_do import CarSeller
from module_admin.entity.vo.car_seller_vo import CarSellerPageModel, CarSellerModel


class CarSellerService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_car_seller_list(cls, query_db: AsyncSession, query_object: CarSellerPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        car_seller_list = await CarSellerDao.get_car_seller_list(query_db, query_object, data_scope_sql, is_page=True)
        return car_seller_list

    @classmethod
    async def get_car_seller_by_id(cls, query_db: AsyncSession, car_seller_id: int) -> CarSellerModel:
        car_seller = await  CarSellerDao.get_by_id(query_db, car_seller_id)
        car_seller_model = CarSellerModel(**CamelCaseUtil.transform_result(car_seller))
        return car_seller_model


    @classmethod
    async def add_car_seller(cls, query_db: AsyncSession, query_object: CarSellerModel) -> CarSellerModel:
        car_seller = await CarSellerDao.add_car_seller(query_db, query_object)
        car_seller_model = CarSellerModel(**CamelCaseUtil.transform_result(car_seller))
        return car_seller_model


    @classmethod
    async def update_car_seller(cls, query_db: AsyncSession, query_object: CarSellerModel) -> CarSellerModel:
        car_seller = await CarSellerDao.edit_car_seller(query_db, query_object)
        car_seller_model = CarSellerModel(**CamelCaseUtil.transform_result(car_seller))
        return car_seller_model


    @classmethod
    async def del_car_seller(cls, query_db: AsyncSession, car_seller_ids: List[str]):
        await CarSellerDao.del_car_seller(query_db, car_seller_ids)


    @classmethod
    async def export_car_seller_list(cls, query_db: AsyncSession, query_object: CarSellerPageModel, data_scope_sql) -> bytes:
        car_seller_list = await CarSellerDao.get_car_seller_list(query_db, query_object, data_scope_sql, is_page=False)
        mapping_dict = {
            'age': '年龄 ',
            'carType': '车辆类型 ',
            'driverYears': '驾龄 ',
            'image': '图片 ',
            'location': '所在位置 ',
            'name': '销售名字 ',
            'price': '价格 ',
            'updateTime': '更新时间 ',
        }
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in car_seller_list
        ]
        binary_data = export_list2excel(new_data)
        return binary_data